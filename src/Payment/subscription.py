class Subscription:
    def __init__(self, id, pl_id, sp_id, tr_id, startDate, endDate, price, priceAD, discountValue, discountDes, isD, isPay, paymentTotal):
        self.id = id
        self.pl_id = pl_id
        self.sp_id = sp_id
        self.tr_id = tr_id
        self.startDate = startDate
        self.endDate = endDate
        self.price = price
        self.priceAD = priceAD
        self.discountValue = discountValue
        self.discountDes = discountDes
        self.isD = isD
        self.isPay = isPay
        self.paymentTotal = paymentTotal

    @classmethod
    def from_json(cls, json):
        return Subscription(
            json['id'],
            json['pl_id'],
            json['sp_id'],
            json['tr_id'],
            json['startDate'],
            json['endDate'],
            json['price'],
            json['priceAD'],
            json['discountValue'],
            json['discountDes'],
            json['isD'],
            json['isPay'],
            json['paymentTotal'],
        )

    def to_json(self):
        return {
            'id': self.id,
            'pl_id': self.pl_id,
            'sp_id': self.sp_id,
            'tr_id': self.tr_id,
            'startDate': self.startDate,
            'endDate': self.endDate,
            'price': self.price,
            'priceAD': self.priceAD,
            'discountValue': self.discountValue,
            'discountDes': self.discountDes,
            'isD': self.isD,
            'isPay': self.isPay,
            'paymentTotal': self.paymentTotal,
        }
