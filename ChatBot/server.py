import queue
import socket
import sys
import threading
import requests
import nltk

# API endpoint for the chatGPT
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

# API KEY
API_KEY = "API_KEY"

# Number of threads that can work parallely
NUM_THREADS = 4

# Using LRU Queue for thread management
LRU_QUEUE = queue.Queue()

# Initializing Queue by adding all the threads in the queue
for i in range(NUM_THREADS):
    LRU_QUEUE.put(i)

# LRU Cache for prompts and responses
prompt_cache = {}
cache_size = 10


def generate_response_using_api(prompt):
    # checking if the prompt is present in the cache
    if prompt in prompt_cache:
        return prompt_cache[prompt]

    # OpenAI API request payload
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "You are a helpful assistant."},
                     {"role": "user", "content": prompt}],
    }

    # OpenAI API request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    # Sending POST request
    response = requests.post(API_ENDPOINT, json=payload, headers=headers)
    response_json = response.json()

    # getting the response and storing it into the cache
    generated_response = response_json["choices"][0]["message"]["content"]
    prompt_cache[prompt] = generated_response

    if len(prompt_cache) > cache_size:
        prompt_cache.pop(next(iter(prompt_cache)))

    return generated_response


def extract_named_entities(message):
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    # Tokenize the user's message into sentences
    sentences = nltk.sent_tokenize(message)
    # Extract named entities from each sentence
    named_entities = []
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.ne_chunk(tagged)
        for entity in entities:
            if hasattr(entity, 'label') and entity.label:
                named_entities.append((entity.label(), ' '.join(child[0] for child in entity.leaves())))

    return named_entities


def handle_client(client_socket, address):
    # Using client IP address as client ID
    client_id = address[0]
    while True:
        # Receiving data from the client
        data = client_socket.recv(1024).decode('utf-8')

        # exit state
        if not data or data.lower() == "exit":
            break

        # Checking if client ID is present in the prompt cache
        if client_id in prompt_cache:
            previous_prompt = prompt_cache[client_id]

            # Checking if the current prompt is the same as the previous prompt
            if data == previous_prompt:
                # Generate a new prompt by appending a space
                data += " "

        # Checking if the "Check Entities" command is received,
        # if yes extract the entities and show it to the user
        if data.lower() == "check entities":
            entities = extract_named_entities(previous_prompt)
            entities_str = "\n".join([f"{entity[0]}: {entity[1]}" for entity in entities])
            client_socket.send(entities_str.encode('utf-8'))
            continue

        # Generating the response
        response = generate_response_using_api(data)

        # Updating prompt cache with the current prompt for the client
        prompt_cache[client_id] = data

        # Update the cache with the generated response if needed
        if data not in prompt_cache:
            prompt_cache[data] = response

        # Send the response back to the client
        client_socket.send(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()


def start_server(host, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, server_port))
    server_socket.listen(5)

    print(f"Server started on {host}:{server_port}")

    while True:
        client_socket, address = server_socket.accept()

        # Assigning a thread to handle the client
        thread_id = LRU_QUEUE.get()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

        # Putting the thread ID back to the queue to maintain LRU algorithm
        LRU_QUEUE.put(thread_id)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
        start_server('localhost', port)
