# from attr import dataclass
#
#
# # def supper_decorator[**P, R]() -> Callable[[Callable[P, R]], Callable[P, R]]:
# #     print("Decorartor:")
# #     def decorator(func: Callable[P, R]) -> Callable[P, R]:
# #         @wraps(func)
# #         def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
# #             print("wrapper", args, kwargs)
# #             result = func(*args, **kwargs)
# #             print("Result", result)
# #             return result
# #         return wrapper
# #
# #     return decorator
#
#
# # @supper_decorator()
# @dataclass
# class Student:
#     name: str
#
#     def get_name(self) -> str:
#         print("get name")
#         return self.name
#
#
# def dynamic_instance_method(self):
#     return f"Value is: {self.value}"
#
#
# class TestStudent:
#     def test_main_flow(self):
#         student = Student(name="manhdt").get_name()
#         obj.dynamic_method = types.MethodType(dynamic_instance_method, obj)
#
#         print(student)
