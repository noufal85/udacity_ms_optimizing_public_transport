import ast
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]


class RubricContractTests(unittest.TestCase):
    def test_required_avro_value_schemas_are_complete(self):
        expected = {
            "arrival_value.json": {"station_id", "train_id", "direction", "line", "train_status", "prev_station_id", "prev_direction"},
            "turnstile_value.json": {"station_id", "station_name", "line"},
            "weather_value.json": {"temperature", "status"},
        }
        for filename, fields in expected.items():
            schema = json.loads((ROOT / "producers/models/schemas" / filename).read_text())
            self.assertEqual({f["name"] for f in schema["fields"]}, fields)

    def test_ksql_turnstile_table_uses_station_id_as_avro_key(self):
        statement = (ROOT / "consumers/ksql.py").read_text()
        self.assertIn("KEY='station_id'", statement)
        self.assertIn("KEY_FORMAT='AVRO'", statement)
        self.assertIn("VALUE_FORMAT='AVRO'", statement)
        self.assertIn("GROUP BY station_id", statement)
        self.assertIn("COUNT(*) AS count", statement)

    def test_turnstile_producer_uses_station_id_as_key(self):
        producer = (ROOT / "producers/models/turnstile.py").read_text()
        schema = json.loads((ROOT / "producers/models/schemas/turnstile_key.json").read_text())
        self.assertEqual([field["name"] for field in schema["fields"]], ["station_id"])
        self.assertIn('"station_id": self.station.station_id', producer)

    def test_required_modules_have_no_assignment_todos(self):
        paths = [
            ROOT / "producers/models/producer.py",
            ROOT / "producers/models/station.py",
            ROOT / "producers/models/turnstile.py",
            ROOT / "producers/models/weather.py",
            ROOT / "producers/connector.py",
            ROOT / "consumers/consumer.py",
            ROOT / "consumers/faust_stream.py",
            ROOT / "consumers/ksql.py",
            ROOT / "consumers/models/line.py",
            ROOT / "consumers/models/weather.py",
        ]
        for path in paths:
            tree = ast.parse(path.read_text())
            todos = [n for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and "TODO" in n.value]
            self.assertFalse(todos, f"unresolved TODO remains in {path}")


if __name__ == "__main__":
    unittest.main()
