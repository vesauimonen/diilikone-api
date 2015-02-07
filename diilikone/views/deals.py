from flask import Blueprint, jsonify, request

from diilikone.extensions import db
from diilikone.models import Deal, User
from diilikone.schemas import DealGroupSchema

deals = Blueprint('deals', __name__, url_prefix='/deals')


@deals.route('', methods=['POST'])
def post():
    data = request.get_json(force=True)
    data, errors = DealGroupSchema().load(data)
    if errors:
        return jsonify({'errors': errors}), 400
    for deal_data in data['deals']:
        salesperson = User(**deal_data['salesperson'])
        deal = Deal(
            size=deal_data['size'],
            deal_group_id=data['deal_group_id'],
            salesperson=salesperson
        )
        db.session.add_all([salesperson, deal])
        db.session.commit()
    return jsonify({}), 200
