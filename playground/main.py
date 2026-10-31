from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

from app.agent import build_agent, run_agent
from app.config import DB_URI
from app.schemas import Draft


EXIT_WORDS = ("quit", "exit", "bye")


def main():
    with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
        # Allow our Draft type to be loaded from checkpoints
        checkpointer.serde = JsonPlusSerializer(allowed_msgpack_modules=[Draft])
        checkpointer.setup()  # create checkpoint tables on first run

        agent = build_agent(checkpointer)

        thread_id = input("Conversation name [default]: ").strip() or "default"
        print(f"Type {', '.join(EXIT_WORDS)} to stop.\n")

        # Chat loop
        while True:
            q = input("You: ").strip()
            if not q:
                continue
            if q.lower() in EXIT_WORDS:
                break

            print(f"\nDraftly:\n{run_agent(agent, q, thread_id)}\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
