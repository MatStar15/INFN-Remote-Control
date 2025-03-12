from celery_app import hello_world

if __name__ == '__main__':
    # Send the task to worker
    result = hello_world.delay()
    print(f"Task sent. ID: {result.id}")

    # Wait for result
    try:
        task_result = result.get(timeout=10)
        print(f"Task completed. Result: {task_result}")
    except Exception as e:
        print(f"Error: {e}")