from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Correction

@csrf_exempt
def correct_sentence(request):
    if request.method == "OPTIONS":
        # Allow CORS/OPTIONS preflight
        response = HttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    if request.method == "POST":
        try:
            import openai, os, json
            from dotenv import load_dotenv

            load_dotenv()
            openai.api_key = os.getenv("OPENAI_API_KEY")

            data = json.loads(request.body)
            sentence = data.get("sentence")

            if not sentence:
                return JsonResponse({"error": "No sentence provided."}, status=400)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that corrects German grammar. Return a corrected sentence, explanation, CEFR difficulty, and a confidence score from 0 to 1."},
                    {"role": "user", "content": f"Bitte korrigiere diesen Satz: {sentence}"}
                ]
            )

            content = response["choices"][0]["message"]["content"]

            # 🔥 PARSE THE RAW TEXT
            corrected = ""
            explanation = ""
            difficulty = ""
            confidence = 0.0

            # Simple parsing by line splitting
            lines = content.split("\n")
            for line in lines:
                line = line.strip()
                if line.lower().startswith("explanation:"):
                    explanation = line.replace("Explanation:", "").strip()
                elif line.lower().startswith("cefr level:"):
                    difficulty = line.replace("CEFR Level:", "").strip()
                elif line.lower().startswith("confidence score:"):
                    confidence_text = line.replace("Confidence Score:", "").strip()
                    try:
                        confidence = float(confidence_text)
                    except:
                        confidence = 0.0
                else:
                    # Assume first line is corrected sentence
                    if corrected == "":
                        corrected = line
                 # ✅ SAVE to database
            Correction.objects.create(
                original_sentence=sentence,
                corrected_sentence=corrected,
                explanation=explanation,
                difficulty=difficulty,
                confidence=confidence
            )
            return JsonResponse({
                "corrected": corrected,
                "explanation": explanation,
                "difficulty": difficulty,
                "confidence": confidence
            })

       
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests allowed."}, status=405)
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')
