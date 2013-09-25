import requests
import pprint


def billSearch(search, per_page, page):

    query_params = {'apikey': apikey,
                    'per_page': per_page,
                    'page': page,
                    'congress': 113,
                    'chamber': 'house',
                    'order': 'introduced_on',
                    'query': search
                    }

    bills_search = 'http://congress.api.sunlightfoundation.com/bills/search'

    response = requests.get(bills_search, params=query_params)
    data = response.json()

    return data


def displayBills(returned_bills):
    i = 0
    for bill in returned_bills:  # search_return['results']
        i += 1
        print i, bill['bill_id']
        print bill['official_title']
        print bill['urls']['congress']
        print ' '


def detailBill(bill_id):
    query_params2 = {'apikey': '002e85a1cf614ff89f6ac3a8837c33f2',
                     'bill_id': bill_id,
                     }

    bill_info = 'http://congress.api.sunlightfoundation.com/bills'
    response2 = requests.get(bill_info, params=query_params2)
    data2 = response2.json()
    cosponsors_count = data2['results'][0]['cosponsors_count']
    pprint.pprint('%s has %d cosponsors.' % (bill_id, cosponsors_count))

### MAIN ###

apikey = '002e85a1cf614ff89f6ac3a8837c33f2'
bpp = 5  # bills per page
pages = 0
current_page = 1

user_input = raw_input('Search for a bill: ')
user_input = user_input.upper()
search_return = billSearch(user_input, bpp, current_page)

return_count = search_return['count']
pages = int(return_count / bpp) + 1  # total pages of bills returned

if return_count > 0:

    displayBills(search_return['results'])

    # pagine results
    while pages > 0:
        pprint.pprint('%d bills matching your criteria were found.'
                      % return_count)

        num_select = ['1', '2', '3', '4', '5']

        if 1 == current_page == pages:  # select bill or quit
            user_cont = raw_input('Select a bill by number, or "q" to quit: ')
            if user_cont in num_select:
                selected_bill = search_return['results'][int(user_cont) - 1]['bill_id']
                detailBill(selected_bill)  # query for specific bill in
            elif user_cont == 'q':
                pages = 0
                print "Quitting BillSearch"
            else:
                pages = 0
                print "Invalid response. Peace out."

        elif 1 == current_page < pages:  # select bill, next page, or quit

            user_cont = raw_input('Select a bill by number, \
                                  type "n" for next page, or "q" to quit: ')

            if user_cont in num_select:
                selected_bill = search_return['results'][int(user_cont) - 1]['bill_id']
                detailBill(selected_bill)  # query for specific bill in
            elif user_cont == 'n':
                current_page += 1
                search_return = billSearch(user_input, bpp, current_page)
                displayBills(search_return['results'])
            elif user_cont == 'q':
                pages = 0
                print "Quitting BillSearch"
            else:
                pages = 0
                print "Invalid response. Peace out."

        elif 1 < current_page < pages:  # select bill, n, p, or q

            user_cont = raw_input('Select a bill by #, \
                                 type "n" for next, \
                                 "p" for previous, or "q" to quit: ')

            if user_cont in num_select:
                selected_bill = search_return['results'][int(user_cont) - 1]['bill_id']
                detailBill(selected_bill)  # query for specific bill in
            elif user_cont == 'n':
                current_page += 1
                search_return = billSearch(user_input, bpp, current_page)
                displayBills(search_return['results'])
            elif user_cont == 'p':
                current_page -= 1
                search_return = billSearch(user_input, bpp, current_page)
                displayBills(search_return['results'])
            elif user_cont == 'q':
                pages = 0
                print "Quitting BillSearch"
            else:
                pages = 0
                print "Invalid response. Peace out"
        elif 1 < current_page == pages:  # select bill, previous page, or quit

            user_cont = raw_input('Select a bill, previous, or quit: ')

            if user_cont in num_select:
                selected_bill = search_return['results'][int(user_cont) - 1]['bill_id']
                detailBill(selected_bill)  # query for specific bill info

            elif user_cont == 'p':
                current_page -= 1
                search_return = billSearch(user_input, bpp, current_page)
                displayBills(search_return['results'])

            elif user_cont == 'q':
                pages = 0
                print "Quitting BillSearch."
            else:
                pages = 0
                print "Invalid response. Peace out."

        else:
                pages = 0
                print "Error: pagination criteria not met."
                pass

else:
    print 'No bills found.'
