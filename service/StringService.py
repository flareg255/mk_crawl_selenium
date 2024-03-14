class StringService:

    def priceStringToNumber(price):
        return str.strip(price).replace(',', '').replace('円', '')

    def spaceAndReturnReplace(string):
        return str.strip(string).replace('\u3000', ' ').replace('\r\n','</br>').replace('\n', '</br>')

    def spaceReplace(string):
        return str.strip(string).replace('\u3000', ' ')