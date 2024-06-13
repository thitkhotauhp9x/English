from dataclasses import dataclass
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch


@dataclass
class ProductionClass:
    product: str


def add(a, b):
    return a + b


@dataclass
class Outer:
    @dataclass
    class Class:
        def method(self):
            pass


class Test(TestCase):
    def test_should_be_called_with_params(self):
        thing = ProductionClass
        thing.method = MagicMock(return_value=3)
        thing.method(3, 4, 5, key="value")
        thing.method.assert_called_with(3, 4, 5, key="value")

    def test_should_raise_an_exception(self):
        mock = Mock(side_effect=KeyError("foo"))
        with self.assertRaises(KeyError) as info:
            mock()
        error: KeyError = info.exception
        self.assertEqual(error.args, ("foo",))

    def test_mock_with_side_effect(self):
        values = {"a": 1, "b": 2, "c": 3}

        def side_effect(arg):
            return values[arg]

        mock = Mock(side_effect=KeyError("foo"))
        mock.side_effect = side_effect

        self.assertEqual((mock("a"), mock("b"), mock("c")), (1, 2, 3))

        mock.side_effect = [5, 4, 3, 2, 1]

        self.assertEqual((mock(), mock(), mock()), (5, 4, 3))

    def test_abc(self):
        # with patch("tests.test.add") as mock:
        #     result = add(1, 2)
        #     ic(result)
        #     mock.assert_called()

        with patch("tests.test.ProductionClass", create=True) as mock:
            instant = mock.return_value
            instant.product = "..."
            pc = ProductionClass("")
            assert pc.product == "..."
            mock.assert_called()

        with patch.object(ProductionClass, "__init__", return_value=None) as mock:
            ...
