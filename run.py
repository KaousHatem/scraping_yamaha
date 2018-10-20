import pandas as pd
import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.pieces-yam.com/"
PIECE_DETACHEE_URL = BASE_URL + "yamaha-moto/affectation_pieces_detachees/"
headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
	} 

def log_i(log,code,ref,link):
	print('[+]---getting info from ref:',ref,'---code:',code,' ',log)

def log_e(log,code,ref,link):
	print('[-]---error in getting info from:',link,'ref:',ref,'---code:',code,' ',log)

def get_references_csv(link):
	df = list(pd.read_csv(link,header=None)[0])
	return df

def get_info_by_ref(log,ref):
	url = PIECE_DETACHEE_URL+ref
	response_ = requests.get(url, headers=headers)
	if response_.status_code == 200:
		log_i(log,response_.status_code,ref,url)
		info = []
		if not('Référence inconnue' in response_.text):
			soup = BeautifulSoup(response_.text,'lxml')
			price_div = soup.find('span',attrs={'itemprop':'price'})
			if price_div:
				price = price_div.get('content')
			else:
				price = None
			table = soup.find('table',attrs={'id':'table_panier_tarif'})
			trs = table.find('tbody').findAll('tr')
			for tr in trs:
				tds = tr.findAll('td')
				ref = tds[0].text.replace(' ','').replace('\n','|').split('|')[1]
				des = tds[1].text
				mod = tds[3].text.replace('Année :',' ').split()
				modele = ' '.join(mod[1:])
				annee = mod[0]
				pays = ' '.join(tds[4].text.replace('\n','').split())
				info.append([ref,des,price,modele,annee,pays])
	else:
		log_e(log,response_.status_code,ref,url)
		
	return info


if __name__ == "__main__":
	refs = get_references_csv('link_in.csv')
	all_info = []
	for ref in refs:
		log = '--- '+str(refs.index(ref)+1)+'/'+str(len(refs))+'---'
		info_ref = get_info_by_ref(log,ref)
		all_info+=info_ref
	df = pd.DataFrame(all_info)
	df.to_csv('result_info.csv')

		
