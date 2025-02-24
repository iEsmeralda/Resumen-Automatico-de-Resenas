#Proyecto Final: Resúmenes de Reseñas Académicas

import pandas as pd
from transformers import pipeline
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

comentarios = pd.read_csv('CSV/Comentarios_Profesores_Generalizado.csv')
listado = pd.read_csv('CSV/Listado_profesores_Generalizado.csv')
comentarios_referencia = pd.read_csv('CSV/Comentarios_Referencia.csv')

try:
    modelo_resumen = pipeline("summarization", model="facebook/bart-large-cnn")
    print("Modelo cargado exitosamente.")
except Exception as e:
    print("Error cargando el modelo:", e)
    #modelo_beto = None
    modelo_resumen = None

def listado_profesores():
    print("Listado de profesores:")
    #Obtenemos el listado
    profesores_unicos = comentarios['Profesor'].unique()
    for index, profesor in enumerate(profesores_unicos):
        print(f"\t{index + 1}. {profesor}")

def ver_comentarios(profesores_unicos):
    try:
        numero_profesor = int(input('Ingrese el numero del profesor: '))
        if 1 <= numero_profesor <= len(profesores_unicos):
            profesor = profesores_unicos[numero_profesor - 1]
            comentarios_profesor = comentarios[comentarios['Profesor'] == profesor]
            if comentarios_profesor.empty:
                print(f"No hay comentarios disponibles para {profesor}.")
                return
            print(f"Comentarios del profesor {profesor}:")
            for index, comentario in comentarios_profesor.iterrows():
                print(f"\t{index+1}. {comentario['Comentario']}")
        else:
            print('Opcion invalida, intente de nuevo')
    except ValueError:
        print('Opcion invalida, intente de nuevo')

def generar_opinion(profesores_unicos):
    try:
        numero_profesor = int(input('Ingrese el numero del profesor: '))
        if 1 <= numero_profesor <= len(profesores_unicos):
            profesor = profesores_unicos[numero_profesor - 1]
            print(f"Generando opinión del profesor {profesor}:")
            comentarios_profesor = comentarios[comentarios['Profesor'] == profesor]["Comentario"]
            if comentarios_profesor.empty:
                print(f"No hay comentarios disponibles para {profesor}.")
                return

            comentarios_profesor = comentarios_profesor.dropna()
            comentarios_profesor = comentarios_profesor.astype(str)

            if len(comentarios_profesor) <= 4:
                print(f"El profesor {profesor} tiene {len(comentarios_profesor)} comentarios. Mostrando todos los comentarios disponibles:")
                for comentario in comentarios_profesor:
                    print(f"- {comentario}")
                return

            elif 5 <= len(comentarios_profesor) < 9:
                texto_base = ' '.join(comentarios_profesor.tolist())
            else:
                texto_base = ' '.join(comentarios_profesor.sample(n=9, random_state=37).tolist())

            print(f"Texto base para generación: {texto_base}")

            if modelo_resumen is None:
                print("El modelo de resumen no está disponible. Verifica su carga.")
                return

            if not texto_base.strip():
                print("No hay suficiente texto base para generar un resumen.")
                return

            try:
                opinion_generada = modelo_resumen(
                    texto_base, max_length=300, min_length=150, do_sample=False
                )[0]['summary_text']
                print("\n############################################\n")
                print(f"Resumen generado: {opinion_generada}")

                return opinion_generada #Obtener la opinion

            except Exception as e:
                print("Error generando la opinión:", e)
                return None
        else:
            print('Opción inválida, intente de nuevo 1')
            return None
    except ValueError:
        print('Opción inválida, intente de nuevo 2')
        return None

# Calcular la métrica de BLEU
def calcular_bleu(opinion_generada, comentarios_ref):
    # Tokenizar los comentarios de referencia y la opinión generada
    referencia_bleu = [ref.split() for ref in comentarios_ref]
    opinion_bleu = opinion_generada.split()

    #BLEU normal
    score_bleu = sentence_bleu(referencia_bleu, opinion_bleu)
    print(f"BLEU score: {score_bleu:.4f}")

    # Configuración para BLEU-1 y suavizado
    score_bleu1 = sentence_bleu(
        referencia_bleu,
        opinion_bleu,
        weights=(1, 0, 0, 0),  # Solo considera unigramas
        smoothing_function=SmoothingFunction().method1  # Aplica suavizado
    )
    print(f"BLEU-1 score: {score_bleu1:.4f}")
    return score_bleu, score_bleu1

# Calcular la métrica de ROUGE
def calcular_rouge(opinion_generada, comentarios_ref):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores_rouge = scorer.score(' '.join(comentarios_ref), opinion_generada)
    print("ROUGE scores:")
    print(f"ROUGE-1: {scores_rouge['rouge1']}") # Unigramas
    print(f"ROUGE-2: {scores_rouge['rouge2']}") # Bigramas
    print(f"ROUGE-L: {scores_rouge['rougeL']}") # Subsecuencia común más larga
    return scores_rouge

def evaluar_opinion(opinion_generada):
    numero_profesor = int(input('Ingrese el numero del profesor nuevamente: '))
    numeros_unicos = comentarios_referencia['Numero'].unique().astype(int)
    if numero_profesor in numeros_unicos:
        comentarios_ref = comentarios_referencia[comentarios_referencia['Numero'].astype(str) == str(numero_profesor)]["Comentario"].dropna() # Sin valores nulos
        print("\n ** Evaluando la opinión generada: **")
        for i, comentario in enumerate(comentarios_ref, 1):
            print(f"Opinión de referencia: {comentario}")
        # Evaluar con BLEU
        print("\nMétrica BLEU:")
        bleu_score = calcular_bleu(opinion_generada, comentarios_ref)
        # Evaluar con ROUGE
        print("\nMétrica ROUGE:")
        rouge_scores = calcular_rouge(opinion_generada, comentarios_ref)
        #return bleu_score, rouge_scores
    else:
        print('No existen comentarios de referencia para ese profesor')
        #return None, None

def sub_menu():
    profesores_unicos = comentarios['Profesor'].unique()
    while True:
        print('MENU')
        print('1. Ver comentarios')
        print('2. Generar opinion')
        print('3. Evaluar opinión generada')
        print('4. Salir')

        try:
            opcion = int(input('Ingrese una opcion: '))
            if opcion == 1:
                ver_comentarios(profesores_unicos)
            elif opcion == 2:
                opinion_generada = generar_opinion(profesores_unicos)
            elif opcion == 3:
                if opinion_generada:
                    #print(opinion_generada)
                    evaluar_opinion(opinion_generada)
                else:
                    print("Primero debe generar una opinión antes de evaluarla.")
            elif opcion == 4:
                break
            else:
                print('Opcion invalida, intente de nuevo')
        except ValueError:
            print('Opcion invalida, intente de nuevo')


if __name__ == '__main__':
    profesores_unicos = comentarios['Profesor'].unique()
    while True:
        print('MENU')
        print('1. Listado de profesores')
        print('2. Salir')

        try:
            opcion = int(input('Ingrese una opcion: '))
            if opcion == 1:
                listado_profesores()
                sub_menu()
            elif opcion == 2:
                break
            else:
                print('Opcion invalida, intente de nuevo')
        except ValueError:
            print('Opcion invalida, intente de nuevo')