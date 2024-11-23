from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from threading import Timer, Thread, Lock


TOKEN_LIMIT_PER_MINUTE = 200


class FakeChatModel(ABC):
    @abstractmethod
    def involve(self) -> int:
        ...



@dataclass
class TokenManager:
    lock: Lock = Lock()
    _remain_tokens: int = field(default=TOKEN_LIMIT_PER_MINUTE, init=False)

    @property
    def remain_tokens(self) -> int:
        return self._remain_tokens

    @remain_tokens.setter
    def remain_tokens(self, value) -> None:
        with self.lock:
            self._remain_tokens = max(0, value)
            print(self._remain_tokens)


def do(timer_threads, token_manager: TokenManager) -> None:
    chat_model = FakeChatModel()
    total_tokens = chat_model.involve()

    token_manager.remain_tokens -= total_tokens

    def update_token():
        token_manager.remain_tokens += total_tokens

    timer = Timer(12, update_token)

    timer.start()
    timer_threads.append(timer)



def main():
    threads = []
    timer_threads = []
    token_manager = TokenManager()

    for _ in range(2):
        thread = Thread(target=do, args=(threads, token_manager,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    for timer_thread in timer_threads:
        timer_thread.cancel()




if __name__ == "__main__":
    main()
