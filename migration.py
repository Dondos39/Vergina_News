import csv
import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VerginaNews.settings")
import django
import uuid
import requests
from PIL import Image
from io import BytesIO
import pandas as pd
import warnings
import numpy as np
from bs4 import BeautifulSoup
warnings.filterwarnings("ignore")
django.setup()

from articles.models import Article
from categories.models import Category, SubCategory
from tags.models import Tags
from authors.models import Author
from tqdm import tqdm

COLS = ['object_id', 'post_author', 'post_date', 'post_date_gmt', 'post_content', 'post_title', 'post_excerpt', 'post_status', 'comment_status', 'ping_status', 'post_password',
'post_name', 'to_ping', 'pinged', 'post_modified', 'post_modified_gmt', 'post_content_filtered', 'post_parent', 'guid', 'menu_order', 'post_type', 'post_mime_type', 'comment_count']

main = pd.read_csv(r"C:\Users\Dondo\Desktop\donos.csv", skiprows=lambda x: x%2 == 1, names=COLS, header=None)
term_relationships = pd.read_csv(r"C:\Users\Dondo\Desktop\n895h5iea_term_relationships.csv")
tax = pd.read_excel(r"C:\Users\Dondo\Desktop\n895h5iea_term_taxonomy.xlsx")
terms = pd.read_csv(r"C:\Users\Dondo\Desktop\n895h5iea_terms.csv")

tax_terms = pd.merge(tax, terms, on='term_id', how='left')
tax_terms.drop(['term_id', 'description', 'term_group', 'Unnamed: 6'],  axis=1, inplace=True)

tax_terms_final = pd.merge(term_relationships, tax_terms, on='term_taxonomy_id', how='left')
tax_terms_final.drop(['term_taxonomy_id', 'term_order'],  axis=1, inplace=True)
tax_terms_final['category'] = tax_terms_final.loc[tax_terms_final['taxonomy']=='category'].name
i = tax_terms_final.groupby('object_id')['name'].apply(','.join).reset_index()

cleaned = pd.merge(tax_terms_final, i, on='object_id', how='left')
cleaned.drop_duplicates(subset=['object_id'], inplace=True)
cleaned.drop(['taxonomy', 'name_x', 'count', 'slug'],  axis=1, inplace=True)
cleaned = cleaned.rename(columns={'name_y': 'tags'})

final = pd.merge(main, cleaned, on='object_id', how='left')
final.drop(['post_date', 'post_status', 'comment_status', 'ping_status', 'post_password', 'post_name', 'to_ping', 'pinged', 'post_modified',
            'post_modified_gmt', 'post_content_filtered', 'comment_count', 'post_type', 'post_mime_type', 'menu_order'],  axis=1, inplace=True)
final['post_author'] = 'News Room'
final = final.dropna(subset=['post_content', 'post_title'])
final['tags'] = final['tags'].str.split(',')
final['sub_category'] = np.nan
final = final.reset_index(drop=True)

final['post_content'] = final['post_content'].str.replace('[ad_1]', '')
final['post_content'] = final['post_content'].str.replace('[ad_2]', '')


for i, row in enumerate(final.itertuples()):
    if str(row.category) == 'nan' and str(row.tags) != 'nan':
        for tag in row.tags:
            if tag == 'ΠΌΛΙΤΙΚΗ':
                final.at[i, 'category'] = 'ΠΌΛΙΤΙΚΗ'
                break
            if tag == 'ΟΙΚΟΝΟΜΙΑ':
                final.at[i, 'category'] = 'ΟΙΚΟΝΟΜΙΑ'
                break
            if tag == 'ΑΘΛΗΤΙΣΜΟΣ':
                final.at[i, 'category'] = 'ΑΘΛΗΤΙΣΜΟΣ'
                break
            if tag == 'Απόψεις':
                final.at[i, 'category'] = 'ΑΠΟΨΕΙΣ'
                break
            if tag == 'ΚΟΣΜΟΣ':
                final.at[i, 'category'] = 'ΚΟΣΜΟΣ'
                break
            if tag == 'ΕΚΠΟΜΠΕΣ':
                final.at[i, 'category'] = 'ΕΚΠΟΜΠΕΣ'
                break
            if tag == 'ΕΛΛΑΔΑ':
                final.at[i, 'category'] = 'ΕΛΛΑΔΑ'
                break

        for tag in row.tags:
            if tag == 'ΚΟΜΜΑΤΑ':
                final.at[i, 'sub_category'] ='ΚΟΜΜΑΤΑ'
                final.at[i, 'category'] = 'ΠΌΛΙΤΙΚΗ'
                break
            if tag == 'ΚΥΒΕΡΝΗΣΗ':
                final.at[i, 'sub_category'] ='ΚΥΒΕΡΝΗΣΗ'
                final.at[i, 'category'] = 'ΠΌΛΙΤΙΚΗ'
                break
            if tag == 'ΒΟΥΛΗ':
                final.at[i, 'sub_category'] ='ΒΟΥΛΗ'
                final.at[i, 'category'] = 'ΠΌΛΙΤΙΚΗ'
                break
            if tag == 'ΔΙΕΘΝΗΣ ΟΙΚΟΝΟΜΙΑ':
                final.at[i, 'sub_category'] ='ΔΙΕΘΝΗΣ ΟΙΚΟΝΟΜΙΑ'
                final.at[i, 'category'] = 'ΟΙΚΟΝΟΜΙΑ'
                break
            if tag == 'ΟΙΚΟΝΟΜΙΚΕΣ ΕΙΔΗΣΕΙΣ':
                final.at[i, 'sub_category'] ='ΟΙΚΟΝΟΜΙΚΕΣ ΕΙΔΗΣΕΙΣ'
                final.at[i, 'category'] = 'ΟΙΚΟΝΟΜΙΑ'
                break

final = final.groupby('category').filter(lambda x : len(x)>10)

for row in tqdm(final.itertuples(), total=final.shape[0]):
    if str(row.category)!='nan':
        try:
            category = Category.objects.get(name=row.category)
        except Category.DoesNotExist:
            category = Category(name=row.category, description=row.category)
            category.save()
    else:
        category = None

    if str(row.sub_category)!='nan':
        try:
            sub_category = SubCategory.objects.get(name=row.sub_category)
        except SubCategory.DoesNotExist:
            sub_category = SubCategory(name=row.sub_category, description=row.sub_category, category=category)
            sub_category.save()
    else:
        sub_category = None

    if str(row.post_date_gmt)!='nan':
        date = row.post_date_gmt
    else:
        date = None

    if row.guid:
        print(row)
        response = requests.get(row.guid).content
        if row.guid.endswith('jpg'):
            try:
                img = Image.open(BytesIO(response))
                id = uuid.uuid4()
                img.save(f"Article_pics/{id}.jpg")
                path = f'Article_pics/{id}.jpg'
            except:
                path = None
        else:

                soup = BeautifulSoup(response, 'html.parser')
                image = soup.find('img', class_='entry-thumb')
                img_url = image.get('src')
                break

    else:
        path = None

    article = Article(title=row.post_title,
                      date_added = date,
                      text = row.post_content,
                      article_pic=path,
                      category = category,
                      sub_category = sub_category)

    try:
        article.save()
    except django.db.utils.IntegrityError:
        continue
    except:
        print(row)

    if str(row.tags)!='nan':
        for row_tag in row.tags:
            try:
                tag = Tags.objects.get(name=row_tag)
                article.tags.add(tag)
            except Tags.DoesNotExist:
                tag_ = Tags(name=row_tag)
                tag_.save()
                article.tags.add(tag_)

    try:
        author = Author.objects.get(name=row.post_author)
        article.author.add(author)
    except Author.DoesNotExist:
        print(row)
        author_ = Author(name=row.post_author)
        author_.save()
        article.author.add(author_)
