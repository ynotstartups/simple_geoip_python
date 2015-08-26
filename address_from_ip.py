'''
The purpose of this file is to prepare a result dict to prepare for getting the address for each ip later on.
However, getting address from ip is not reliable, search google for more understanding of ip address.
This program make use of maxmind public database, credit to MaxMind, Inc.
This product includes GeoLite data created by MaxMind, available from http://www.maxmind.com.

Please read main function for example usage.
'''

def return_address_from_ip_list(ip_list,version = 'efficient'):
	'''
	This function returns a result_dict for preparing for the later usage.
	Needs to notice that this function only look at the first three number of the ip address, the reason is
	if we only interest in city, the first three number is good enough.

	Parameters
	-----------
	ip_list : list or string
		list :
		a list of ip address for getting address.
		example, ['82.110.141.43','82.110.141.42','82.110.141.42']

		string : 
		an ip address
		example,'82.110.141.43'

	version : string, optional
		'efficient' or 'precise', choose the method for getting the address.
		'efficient' : Since it only works with the first three number of the ip address, 'efficient' method takes 
		a look at whether the database has the first three number and dot zero, (i.e. first.three.number.0), 
		if it doesn't not has this ip, then consider there is no data.
		'precise' : this method takes a look at all the ip address in database starts with first three number, 
		(i.e. first.three.number.0, first.three.number.1 ...), then select the none 'null' data.

	Returns
	--------
	result_dict : dict
		A dict with the first three number of ip as keys and geodata dict as data.
		example:{'82.110.141': {'continent_name': 'Europe', 'country_name': 'United Kingdom', 'city_name': nan},...}
	'''
	import pandas as pd
	from sys import path
	current_path = path[0]

	# input only one ip handling 
	if type(ip_list) == str:
		ip_list = [ip_list]

	# read files
	csv_directory = current_path + '/database/GeoLite2-City-Blocks-IPv4.csv'
	prepare_ip_to_geo_id_df = pd.read_csv(csv_directory,usecols = ['network','geoname_id'])

	csv_directory = current_path + '/database/GeoLite2-City-Locations-en.csv'
	geo_id_to_address = pd.read_csv(csv_directory,
										usecols = ['geoname_id','continent_name','country_name','city_name'])

	# clean up data
	prepare_ip_to_geo_id_df['network'] = prepare_ip_to_geo_id_df['network'].apply(lambda x: x[:x.rfind('.')])
	
	ip_list = [i[:i.rfind('.')] for i in ip_list]# restyle the ip_list
	result_dict = {}
	for ip in ip_list:
		# change the format of the ip
		ip_to_geo_id_df = prepare_ip_to_geo_id_df[prepare_ip_to_geo_id_df['network']==ip]

		if len(ip_to_geo_id_df) == 0:# no data
			data_dict =  {'continent_name':None,'country_name':None,'city_name':None}
			result_dict[ip] = data_dict

		elif version == 'efficient':
			# take the first element from geo_id
			geo_id = ip_to_geo_id_df['geoname_id'].values[0]
			data = geo_id_to_address[geo_id_to_address['geoname_id'] == int(geo_id)]
			result_dict[ip] = data[['continent_name','country_name','city_name']].squeeze().to_dict()

		elif version == 'precise':
			geo_id = ip_to_geo_id_df['geoname_id']
			geo_id = geo_id.unique()
			if len(geo_id) == 1:
				indexing_list = geo_id_to_address['geoname_id'] == int(geo_id[0])
			else:# length > 1
				indexing_list = geo_id_to_address['geoname_id'] == int(geo_id[0])
				for geo_id_values in geo_id[1:]:
					indexing_list = indexing_list | (geo_id_to_address['geoname_id'] == int(geo_id_values))

			data = geo_id_to_address[indexing_list]

			for i in data['continent_name']:
				if not pd.isnull(i):
					continent_name = i
					break
				else:
					continent_name = None

			for i in data['country_name']:
				if not pd.isnull(i):
					country_name = i
					break
				else:
					country_name = None

			for i in data['city_name']:
				if not pd.isnull(i):
					city_name = i
					break
				else:
					city_name = None

			data_dict = {'continent_name':continent_name,
						'country_name':country_name,
						'city_name':city_name}
			result_dict[ip] = data_dict

		else:
			raise ValueError('Unknown Version Parameter, should be \'efficient\'|\'precise\'' )

	return result_dict

def return_address_dict(ip_list,result_dict):

	'''
	Returns a dict with ip as key, geo_data dict as data.

	Parameters
	-----------
	ip_list : list or string
		list :
		a list of ip address for getting address.
		example, ['82.110.141.43','82.110.141.42','82.110.141.42']

		string : 
		an ip address
		example,'82.110.141.43'

	result_dict : dict
		A dict with the first three number of ip as keys and geodata dict as data.
		example:{'82.110.141': {'continent_name': 'Europe', 'country_name': 'United Kingdom', 'city_name': nan},...}
		This is the output of return_address_from_ip_list function.

	Returns
	--------
	final_result_dict : dict
		a dict with ip as key, geo_data dict as data.
		example, {'82.110.141.43': {'continent_name': 'Europe', 'country_name': 'United Kingdom', 'city_name': nan}, 
					'82.110.141.42': {'continent_name': 'Europe', 'country_name': 'United Kingdom', 'city_name': nan}...}

	'''

	# input only one ip handling 
	if type(ip_list) == str:
		ip_list = [ip_list]

	final_result_dict = {}
	for ip in ip_list:
		modified_ip = ip[:ip.rfind('.')]
		final_result_dict[ip] = result_dict[modified_ip]
	return final_result_dict

def address_from_ip(ip_list):
	'''
	A wrapper function returns a geo_information dict which using the ip as dict keys.

	Parameters
	-----------
	ip_list : list or string
		list :
		a list of ip address for getting address.
		example, ['82.110.141.43','82.110.141.42','82.110.141.42']

		string : 
		an ip address
		example,'82.110.141.43'

	Returns
	--------
	final_dict : dict
		a dict with ip as key, geo_data dict as data.
		example, {'82.110.141.43': {'continent_name': 'Europe', 'country_name': 'United Kingdom', 'city_name': nan}, 
					'82.110.141.42': {'continent_name': 'Europe', 'country_name': 'United Kingdom', 'city_name': nan}...}

	'''
	geo_dict = return_address_from_ip_list(ip_list,version = 'efficient')# choose method 'efficient'
	final_dict = return_address_dict(ip_list,geo_dict)
	return final_dict

def main():
	# for testing
	ip_list = ['82.110.141.43','82.110.141.42','82.110.141.42']
	ip = '82.110.141.43'
	final_dict_0 = address_from_ip(ip_list)
	final_dict_1 = address_from_ip(ip)
	print(final_dict_0)
	print(final_dict_1)

if __name__ == '__main__':
	main()