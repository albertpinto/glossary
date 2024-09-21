import sys
from glossary.crew import GlossaryCrew

def run():
    """
    Run the crew and convert the output to Markdown.
    """
    inputs = {
        'topic': 'Prompt Engineering'
    }
    GlossaryCrew().run_and_convert(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "Supportvectors courses in Fremont,CA"
    }
    try:
        GlossaryCrew().crew().train(n_iterations=int(sys.argv[2]), filename=sys.argv[3], inputs=inputs)
    except Exception as e:
        print(f"An error occurred while training the crew: {e}")
        sys.exit(1)

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        GlossaryCrew().crew().replay(task_id=sys.argv[2])
    except Exception as e:
        print(f"An error occurred while replaying the crew: {e}")
        sys.exit(1)

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "Supportvectors courses in Fremont,CA"
    }
    try:
        GlossaryCrew().crew().test(n_iterations=int(sys.argv[2]), openai_model_name=sys.argv[3], inputs=inputs)
    except Exception as e:
        print(f"An error occurred while testing the crew: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [run|train|replay|test] [args...]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)