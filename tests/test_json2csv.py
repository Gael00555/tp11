"""Tests unitarios de tp11.json2csv."""

import argparse
import io

import pytest

from tp11 import BUILD, __version__
from tp11.json2csv import (
    Json2CsvError,
    flatten,
    main,
    parse_delimiter,
    parse_json,
    read_text,
    to_csv,
    write_text,
)


# --- parse_delimiter -------------------------------------------------------
def test_parse_delimiter_valid():
    assert parse_delimiter(";") == ";"
    assert parse_delimiter("\\t") == "\t"


@pytest.mark.parametrize("value", ["", ",,", '"', "\n"])
def test_parse_delimiter_invalid(value):
    with pytest.raises(argparse.ArgumentTypeError):
        parse_delimiter(value)


# --- parse_json ------------------------------------------------------------
def test_parse_json_object_and_list():
    assert parse_json('{"a": 1}') == [{"a": 1}]
    assert parse_json('[{"a": 1}, {"b": 2}]') == [{"a": 1}, {"b": 2}]


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("", "vacía"),
        ("   ", "vacía"),
        ("{malo", "JSON inválido"),
        ("[1, 2]", "no es un objeto"),
        ('"hola"', "objeto o una lista"),
        ("3", "objeto o una lista"),
    ],
)
def test_parse_json_errors(text, message):
    with pytest.raises(Json2CsvError, match=message):
        parse_json(text)


# --- flatten / to_csv ------------------------------------------------------
def test_flatten_nested_and_types():
    record = {
        "a": 1,
        "b": {"c": True, "d": None},
        "e": [1, "x"],
        "f": {},
        "g": 2.5,
        "h": "t",
    }
    assert flatten(record) == {
        "a": "1",
        "b.c": "true",
        "b.d": "",
        "e": '[1, "x"]',
        "f": "{}",
        "g": "2.5",
        "h": "t",
    }


def test_to_csv_union_of_columns():
    text = to_csv([{"id": 1, "n": "Ana"}, {"id": 2, "x": "y"}], ",")
    assert text == "id,n,x\n1,Ana,\n2,,y\n"


def test_to_csv_delimiter_and_quoting():
    text = to_csv([{"a": "x;y", "b": 'say "hi"'}], ";")
    assert text == 'a;b\n"x;y";"say ""hi"""\n'


def test_to_csv_empty():
    assert to_csv([], ",") == ""
    assert to_csv([{}], ",") == ""


# --- read_text -------------------------------------------------------------
def test_read_text_file(tmp_path):
    path = tmp_path / "a.json"
    path.write_text("[1]", encoding="utf-8")
    assert read_text(str(path)) == "[1]"


def test_read_text_stdin(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("hola"))
    assert read_text(None) == "hola"


def test_read_text_missing(tmp_path):
    with pytest.raises(Json2CsvError, match="no existe"):
        read_text(str(tmp_path / "nada.json"))


def test_read_text_directory(tmp_path):
    # Linux: IsADirectoryError; Windows: PermissionError.
    with pytest.raises(Json2CsvError, match="directorio|permiso"):
        read_text(str(tmp_path))


def test_read_text_invalid_utf8(tmp_path):
    path = tmp_path / "b.json"
    path.write_bytes(b"\xff\xfe")
    with pytest.raises(Json2CsvError, match="UTF-8"):
        read_text(str(path))


# --- write_text ------------------------------------------------------------
def test_write_text_file(tmp_path):
    path = tmp_path / "o.csv"
    write_text(str(path), "a,b\n1,2\n")
    assert path.read_text(encoding="utf-8") == "a,b\n1,2\n"


def test_write_text_stdout(capsys):
    write_text(None, "hola\n")
    assert capsys.readouterr().out == "hola\n"


def test_write_text_directory(tmp_path):
    with pytest.raises(Json2CsvError, match="directorio|permiso"):
        write_text(str(tmp_path), "x")


# --- main ------------------------------------------------------------------
def test_main_file_to_file(tmp_path, capsys):
    source = tmp_path / "in.json"
    source.write_text('[{"id": 1, "n": {"x": 2}}]', encoding="utf-8")
    target = tmp_path / "out.csv"
    assert main(["-i", str(source), "-o", str(target)]) == 0
    assert target.read_text(encoding="utf-8") == "id,n.x\n1,2\n"
    assert capsys.readouterr().out == ""


def test_main_stdin_to_stdout(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO('{"a": 1, "b": 2}'))
    assert main([]) == 0
    assert capsys.readouterr().out == "a,b\n1,2\n"


def test_main_custom_delimiter(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO('{"a": 1, "b": 2}'))
    assert main(["-d", ";"]) == 0
    assert capsys.readouterr().out == "a;b\n1;2\n"


def test_main_error_returns_1(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("{malo"))
    assert main([]) == 1
    assert "json2csv: error" in capsys.readouterr().err


def test_main_error_does_not_create_output(tmp_path, monkeypatch):
    target = tmp_path / "o.csv"
    monkeypatch.setattr("sys.stdin", io.StringIO("{malo"))
    assert main(["-o", str(target)]) == 1
    assert not target.exists()


def test_main_invalid_delimiter():
    with pytest.raises(SystemExit) as info:
        main(["-d", ",,"])
    assert info.value.code == 2


def test_main_missing_argument_value():
    with pytest.raises(SystemExit) as info:
        main(["-i"])
    assert info.value.code == 2


def test_main_broken_pipe(monkeypatch):
    def broken(path, text):
        raise BrokenPipeError

    monkeypatch.setattr("sys.stdin", io.StringIO('{"a": 1}'))
    monkeypatch.setattr("tp11.json2csv.write_text", broken)
    assert main([]) == 0


def test_version_option(capsys):
    with pytest.raises(SystemExit) as info:
        main(["--version"])
    assert info.value.code == 0
    out = capsys.readouterr().out
    assert __version__ in out
    assert BUILD in out


# --- errores de E/S simulados ----------------------------------------------
def _raiser(error):
    def fail(*args, **kwargs):
        raise error

    return fail


def test_read_text_permission_error(monkeypatch):
    monkeypatch.setattr("tp11.json2csv.open", _raiser(PermissionError), raising=False)
    with pytest.raises(Json2CsvError, match="permiso para leer"):
        read_text("x.json")


def test_read_text_generic_os_error(monkeypatch):
    monkeypatch.setattr("tp11.json2csv.open", _raiser(OSError("fallo")), raising=False)
    with pytest.raises(Json2CsvError, match="error leyendo"):
        read_text("x.json")


def test_write_text_permission_error(monkeypatch):
    monkeypatch.setattr("tp11.json2csv.open", _raiser(PermissionError), raising=False)
    with pytest.raises(Json2CsvError, match="permiso para escribir"):
        write_text("x.csv", "a")


def test_write_text_generic_os_error(monkeypatch):
    monkeypatch.setattr("tp11.json2csv.open", _raiser(OSError("fallo")), raising=False)
    with pytest.raises(Json2CsvError, match="error escribiendo"):
        write_text("x.csv", "a")
