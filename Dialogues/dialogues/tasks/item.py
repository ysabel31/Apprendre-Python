import celery
from models.item import ItemModel
import app

celery_app = app.create_celery_app()

@celery_app.task
def add_ASIN_LINK_AMAZON(_id):
    item = ItemModel.find_by_id(_id)

    """     
    if item:
       
        urlAmazon  = "http://webservices.amazon.com/onca/xml"
        urlAmazon += "?Service=AWSECommerceService"
        urlAmazon += "?AWSAccessKeyId="+AWS_ACCESS_KEYID
        urlAmazon += "?AssociateTag="+ASSOCIATE_TAG
        urlAmazon += "&Operation=ItemLookup"
        urlAmazon += "&ItemId="+item.ASIN
        urlAmazon += "&Timestamp=[YYYY-MM-DDThh:mm:ssZ]"
        urlAmazon += "&Signature=[Request Signature]"
        item.ASIN_LINK_AMAZON = urlAmazon

        item.save_to_db()
    """ 
    
    return True

    #return False