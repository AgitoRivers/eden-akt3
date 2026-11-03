"""Actual HTTP transport and asset route smoke test; disposable game and configuration."""
import http.client
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
import random
import warnings
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lauf_test
from lauf_test import eden
from http.server import ThreadingHTTPServer


class HTTPTest(unittest.TestCase):
    def test_real_job_and_asset_routes(self):
        with tempfile.TemporaryDirectory(prefix="eden_dice_http_") as folder:
            lauf_test.vorbereiten("eden_rise", folder)
            eden.modul_laden()["schnelljobs"] = True   # eden_rise: Schnelljobs abgeschaltet (29.10.2026), hier die Wuerfel-Route
            warnings.simplefilter("ignore", ResourceWarning)  # legacy fixture opens JSON without context managers
            random.seed(7)
            job = None
            protocol = {"schritte": [], "erledigt": {}}
            z = eden.aktion("neu", {})
            for _ in range(180):
                if z.get("persona") and z["werte"].get("energie", 0) > 0:
                    jobs = eden.handel.jobs_heute(z, eden.modul_laden(), eden.showrunner.vorrat(eden.moddir()))
                    if jobs:
                        job = {"id": jobs[0]["id"]}
                        break
                action = lauf_test.schritt(z, protocol)
                if not action:
                    break
                name, data = action
                if name == "_tagesarbeit":
                    continue
                z = eden.aktion(name, data)
            self.assertIsNotNone(job, "No job available in disposable fixture")
            server = ThreadingHTTPServer(("127.0.0.1", 0), eden.Handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            def request(method, path, data=None):
                connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=15)
                connection.request(method, path, json.dumps(data) if data is not None else None,
                                   {"Content-Type": "application/json"})
                response = connection.getresponse()
                result = response.status, response.getheader("Content-Type"), response.read()
                connection.close()
                return result
            try:
                status, _, raw = request("POST", "/api/job", job)
                self.assertEqual(status, 200)
                notice = json.loads(raw)["wuerfel_anzeige"]
                self.assertEqual(len(notice["rolls"]), 1)
                self.assertIn(notice["rolls"][0]["probe"]["wurf"], range(1, 21))
                for _ in range(2):
                    status, _, raw = request("GET", "/api/stand")
                    self.assertEqual(status, 200)
                    self.assertNotIn("wuerfel_anzeige", json.loads(raw))
                for filename, mime in (("eden-dice.js", "text/javascript"),
                                       ("eden-dice.css", "text/css"),
                                       ("assets/critical-success.webp", "image/webp")):
                    status, content_type, raw = request("GET", "/plugins/eden-dice/" + filename)
                    self.assertEqual(status, 200)
                    self.assertEqual(content_type, mime)
                    self.assertTrue(raw)
                for path in ("/plugins/eden-dice/../../eden-config.json",
                             "/plugins/eden-dice/%2e%2e/%2e%2e/eden.py",
                             "/plugins/eden-dice/assets/missing.webp"):
                    self.assertEqual(request("GET", path)[0], 404)
                self.assertNotIn("wuerfel_anzeige", eden.aktiv())
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
