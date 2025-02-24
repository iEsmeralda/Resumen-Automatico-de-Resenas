# Proyecto: Resúmenes de Reseñas Académicas
Para poder ejecutarlo debe instalarse las siguientes librerias con el siguiente comando:
> pip install Selenium beautifulsoup4 tf-keras rouge_score transformers nltk

Sobre los archivos:

1. [Extractor_listado.py](Extractor_listado.py): Este archivo es el extractor del listado general de los profesores de la pagina principal, el cual es el siguiente [Listado_profesores.csv](CSV/Listado_profesores.csv)
2. [Extractor_links.py](Extractor_links.py): Extractor de los enlaces de las paginas que contienen los comentarios sobre los profesores, el archivo que nos da es [links.txt](links.txt)
3. [Extractor_Comentarios.py](Extractor_Comentarios.py): Extractor de los comentarios de los profesores, los cuales se almacenan en el archivo [Comentarios_Profesores.csv](CSV/Comentarios_Profesores.csv)
4. [Estandarizador_comentarios.ipynb](Estandarizador_comentarios.ipynb): Este notebook estandariza los nombres de los profesores, pues ocurría el problema de repeticion de nombres dado que estaban separados con comas o guiones y/o por los mismos acentos se duplicaban los nombres. Los nombre estandarizados están contenidos en[Comentarios_Profesores_Generalizado](CSV/Comentarios_Profesores_Generalizado.csv) 
5. El proyecto tiene 2 archivos [Proyecto final NLP.py](Proyecto%20final%20NLP.py) y [Proyecto final NLP.ipynb](Proyecto%20final%20NLP.ipynb), ambos funcionan solo que uno es un archivo .py y el otro es un notebook.
6. [Comentarios_Referencia.csv](CSV/Comentarios_Referencia.csv): Este csv contiene los comentarios hechos por nosotros que nos ayudan al momento de realizar las métricas.