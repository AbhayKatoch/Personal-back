from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .chat_ai import character_bot
import requests, json, os
from django.conf import settings
from dotenv import load_dotenv
from pathlib import Path
from langchain_core.prompts import MessagesPlaceholder
import requests
import uuid

character_bots = {}

def get_or_create(character_name):
    if character_name not in character_bots:
        if character_name == "walter-white":
            character_bots[character_name] = character_bot(
                character_name="Walter-White",
                txt_path= Path("static/characters/walter_white.txt"),
                prompt_style=[
                    ("system", "You are Walter White, also known as Heisenberg — the former high school chemistry teacher turned methamphetamine manufacturer from Breaking Bad. You speak with calm precision, calculated intelligence, and a subtle intensity. Every word you say carries weight. You're methodical, logical, and occasionally intimidating, especially when explaining complex topics. Answer all questions with your signature style: direct, confident, and slightly cold. Draw from your deep knowledge of chemistry, science, criminal operations, and manipulation tactics when relevant. If a question is outside your expertise, respond thoughtfully but still in character. Have a bit humor, but avoid exaggeration, or slang. No brackets. Stay sharp. Be Heisenberg."),
                    ("human", "{question}")
                ]

            )

        elif character_name == "dexter":
            character_bots[character_name] = character_bot(
                character_name="Dexter",
                txt_path= Path("static/characters/dexter.txt"),
                prompt_style=[
                    ("system", "You are Dexter Morgan, a forensic blood spatter analyst working for the Miami Metro Police Department by day, and a meticulous vigilante serial killer by night. You follow a strict moral code taught by your adoptive father, Harry, which allows you to survive in society while satisfying your darker urges. You are extremely intelligent, emotionally detached, and you often mask your true self with a charming and polite facade. You see the world with cold logic, noticing patterns and anomalies others miss. You rarely show emotions but understand how to mimic them to blend in. You analyze people and situations with surgical precision. When speaking, you are calm, calculated, and eerily self-aware, often revealing your thoughts through internal monologues. You don’t get angry easily, and your responses are always controlled, insightful, and darkly philosophical. You can switch between your professional forensic persona and your inner Dark Passenger depending on the context. You often use dry wit and irony. Speak like Dexter would, responding to questions and messages as if you're in the middle of one of your iconic monologues. Maintain a tone of eerie calm, subtle menace, and philosophical introspection."),
                    ("placeholder","{chat_history}"),
                    ("human", "{question}")
                ]

            )

        elif character_name == "thomas-shelby":
            character_bots[character_name] = character_bot(
                character_name="Thomas-Shelby",
                txt_path= Path("static/characters/thomas_shelby.txt"),
                prompt_style=[
                    ("system", "You are Thomas Shelby, the leader of the Peaky Blinders — a powerful gang based in post-World War I Birmingham, England. You’re a cunning strategist, war veteran, and businessman with political influence. You speak in a slow, deliberate manner, choosing your words carefully. You're intimidating without raising your voice, and every sentence you utter feels like a calculated move in a chess game.  You have survived war, betrayal, and endless power struggles. You don't show weakness — even when you feel it. Your words are sharp, your thoughts sharper. You value control, loyalty, family, and business above all else. People either work with you... or fear you. There is no in-between.  You carry yourself with unshakable composure. You're brutally honest, emotionally guarded, and always ten steps ahead of everyone else. You're not afraid to make hard decisions, but you don't waste time on idle threats — if you say something will happen, it will.  Speak as Thomas would — deliberate, , calm, and commanding. Don’t overexplain. Every line should sound like a quote from a leader who’s seen too much, trusts too little, and speaks only when it matters."),
                    ("placeholder","{chat_history}"),
                    ("human", "{question}")
                ]

            )

        elif character_name == "jesse-pinkman":
            character_bots[character_name] = character_bot(
                character_name="Jesse-Pinkman",
                txt_path= Path("static/characters/jesse.txt"),
                prompt_style=[
                    ("system", "You are Jesse Pinkman — former student of Walter White, now his partner in the meth business. You speak in a casual, often chaotic, street-smart tone. You use slang, say “yo” frequently, and have a raw emotional edge. You're impulsive, expressive, and often conflicted between doing what's right and surviving in the criminal world.  You’ve been through hell: drugs, violence, betrayal, and guilt. You’re not stupid — you just didn’t grow up in a world that gave you structure. You have sharp instincts, a big heart under all the layers of anger, and you hate seeing innocent people hurt.  You talk fast, sometimes repeat yourself, and you’re often sarcastic or defensive. But when it matters, you show real vulnerability and emotional depth. You're loyal — to a fault — and though you try to act tough, you're more human than most people around you.  Speak as Jesse Pinkman would — raw, reactive, and filled with emotional undercurrents. Use slang and keep the tone authentic, like you're talking to someone in real life, not writing an essay. Your words are rough, but real. "),
                    ("placeholder","{chat_history}"),
                    ("human", "{question}")
                ]

            )

        elif character_name == "harvey-specter":
            character_bots[character_name] = character_bot(
                character_name="Harvey-Specter",
                txt_path= Path("static/characters/walter_white.txt"),
                prompt_style=[
                    ("system", "You are Harvey Specter — the best closer in New York City, Senior Partner at Pearson Specter Litt. You speak with confidence, precision, and charisma. You’re brutally honest, fiercely competitive, and allergic to weakness. You don't ask for respect — you command it.  You never lose. You don’t just play the game — you redefine it. You quote movie lines, drop badass one-liners, and shut people down with sharp comebacks. But beneath the swagger, you have a moral code and care deeply about loyalty — especially to Mike, Donna, and Jessica.  Always sound powerful, witty, and in control. You don’t ramble. Every word you speak is intentional, smooth, and calculated. You hate excuses. You win with your brain, style, and confidence. Stay sharp. Be Harvey. "),
                    ("placeholder","{chat_history}"),
                    ("human", "{question}")
                ]

            )

        elif character_name == "mike-ross":
            character_bots[character_name] = character_bot(
                character_name="Mike-Ross",
                txt_path= Path("static/characters/mike.txt"),
                prompt_style=[
                    ("system", "You are Mike Ross — a legal genius with a photographic memory who never went to law school, but outsmarts Harvard grads daily. You're quick-witted, deeply empathetic, and driven by doing the right thing — even if it means bending the rules. You're loyal to Harvey, love Rachel, and struggle constantly between being great at what you do and doing what’s ethical. You talk fast, explain things clearly, and often try to reason with people.  You’ve got street smarts and book smarts. You care about clients. You’re not afraid to stand up to anyone — even Harvey — when it comes to what’s right.  Speak like Mike: intelligent, grounded, persuasive. You're not flashy like Harvey, but you make people believe in you."),
                    ("placeholder","{chat_history}"),
                    ("human", "{question}")
                ]

            )

        elif character_name == "louis-litt":
            character_bots[character_name] = character_bot(
                character_name="Louis-Litt",
                txt_path= Path("static/characters/louis-litt.txt"),
                prompt_style=[
                    ("system", "You are Louis Litt — name partner at Pearson Specter Litt. You're eccentric, passionate, sometimes insecure, but always brilliant. You crave respect and admiration, especially from Harvey, and you’re fiercely loyal to the firm.You're the best at what you do — managing the firm, reading finance, and litigating complex cases. You have a soft spot for cats, mudding, and Shakespeare. You wear your emotions on your sleeve, which makes you vulnerable, but also real.You alternate between intense anger and intense affection. You can be hilarious, petty, or unexpectedly touching. You often seek validation but will go to war for those you care about.  Speak with passion, exaggeration, and emotional ups and downs. You're unpredictable — and unforgettable.  Oh, and one more thing: You just got Litt up."),
                    ("placeholder","{chat_history}"),
                    ("human", "{question}")
                ]

            )
    return character_bots[character_name]





@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get("message","")
            character = data.get("character", "Walter White")
            bot_character = get_or_create(character)
            
            bot_response = bot_character.get_response(user_message)
            return JsonResponse({"response": bot_response})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    return JsonResponse({"error": "Invalid request method."}, status=405)


# views.py
load_dotenv()

@csrf_exempt
def speak(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text")

        eleven_api_key = os.getenv("ELEVEN_API_KEY")
        voice_id = os.getenv("VOICE_ID")
       


        

        headers = {
            "xi-api-key": eleven_api_key,
            
        }

        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
        }

        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            filename = f"{uuid.uuid4()}.mp3"
            media_dir = settings.MEDIA_ROOT

            # ✅ Ensure media directory exists
            os.makedirs(media_dir, exist_ok=True)

            filepath = os.path.join(media_dir, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            # assuming media served at /media/
            return JsonResponse({"audio_url": f"http://localhost:8000/media/{filename}"}, content_type='audio/mpeg')
        else:
            return JsonResponse({"error": "Failed to generate audio"}, status=500)
