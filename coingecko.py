import requests
import tablib
import time

def main():
    list_api = 'https://api.coingecko.com/api/v3/coins/list'
    coin_api = 'https://api.coingecko.com/api/v3/coins/%s?localization=false&tickers=false&market_data=false&sparkline=false'
    fields = ['id', 'symbol', 'name', 'coingecko_score', 'developer_score', 'community_score', 'liquidity_score', 'public_interest_score']
    iterate_fields = ['community_data', 'developer_data', 'public_interest_stats']


    coins = requests.get(list_api).json()
    coin_ids = [coin.get('id') for coin in coins]
    coin_details = []
    headers = fields + ['description'] # initialise
    for i, coin_id in enumerate(coin_ids):
        print("Processing Coin (%s): %s" % (i, coin_id))
        coin_detail = requests.get(coin_api % coin_id).json()
        row = []
        for field in fields:
            row.append(coin_detail.get(field))
        row.append(coin_detail.get('description').get('en'))
        
        for iterate_field in iterate_fields:
            iterate_detail = coin_detail.get(iterate_field)
            for key, value in iterate_detail.items():
                row.append(value)
                # Build the headers on the first iteration
                if i ==0:
                    headers.append(iterate_field + '_' + key)
        row.append(coin_detail.get('ico_data', {}).get('kyc_required'))
        coin_details.append(tuple(row))
    # Last field after the auto-generated ones
    headers.append('kyc_required')
    data = tablib.Dataset(*coin_details, headers=headers)
    open('coins.xls', 'wb').write(data.xls)

if __name__ == '__main__':
    main()
