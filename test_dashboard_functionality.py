import unittest

class TestDashboard(unittest.TestCase):
    
    def test_dashboard_imports(self):
        try:
            import dashboard
        except Exception as e:
            self.fail(f"Dashboard script failed to import: {e}")

if __name__ == "__main__":
    unittest.main()
