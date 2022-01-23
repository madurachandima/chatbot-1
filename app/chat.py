import random
import json
import torch
import numpy as np
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from predict_illnes import get_illness

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('train_data.json', 'r') as f:
    intents = json.load(f)

with open('symptoms_questions.json', 'r') as q:
    questions = json.load(q)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def call_chatbot(ws):
    bot_name = "Jon"
    ws.send("How can i help you ?")

    symptoms_answers_array = []

    while True:
        sentence = ws.receive()

        if sentence == "quit":
            symptoms_answers_array.clear()
            break

        sentence = tokenize(sentence)
        x = bag_of_words(sentence, all_words)
        x = x.reshape(1, x.shape[0])
        x = torch.from_numpy(x).to(device)

        output = model(x)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    print(tag)
                    ws.send(f"{bot_name} : {random.choice(intent['responses'])}")
                    if tag == "sick":
                        handel_sik_dog(ws, bot_name, symptoms_answers_array)
        else:
            ws.send(f"{bot_name} : Im sorry i dont understand your question")
            # print(f"{bot_name}: Im sorry i dont understand your question")


def handel_sik_dog(ws, bot_name, symptoms_answers_array):
    question_number = 0
    isStartAskQuestions: bool = False
    if not isStartAskQuestions and question_number < 14:

        sentence = ws.receive()
        if str(sentence).upper() == "YES":

            while question_number < len(questions['intents']):
                # print("inside while")
                # print(len(questions['intents']))
                isStartAskQuestions = True
                ws.send(f"{bot_name} : {questions['intents'][question_number]['responses']}")

                sentence = ws.receive()
                if str(sentence).upper() == "QUIT":
                    symptoms_answers_array.clear()
                    break

                if str(sentence).upper() == "YES" or str(sentence).upper() == "NO":
                    symptoms_answers_array.append({str(
                        questions['intents'][question_number]['tag']).upper(): str(sentence).upper()})
                    question_number = question_number + 1
                    # print(symptoms_answers_array)
                else:
                    ws.send(f"{bot_name} : Your answer is incorrect if you want to exit type quit")

            if question_number == 14:
                response = get_illness(symptoms_answers_array)
                ws.send(response)
                symptoms_answers_array.clear()
        else:
            print("return another question.....")
            # return
    else:
        print("Another questions")
        # another response
