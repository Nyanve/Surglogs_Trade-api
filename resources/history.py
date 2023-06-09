from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request, jsonify
from sqlalchemy import or_
import logging

from db import db
from models import HistoryModel
from schemas import HistorySchema, SearchHistorySchema

blp = Blueprint("History", "history", description="Operations on history.")

@blp.route("/exchanges/history_log")
# This route will return all the history of trades in the database  
class History(MethodView):
    # This route will return the whole history of trades 
    @blp.response(200, HistorySchema(many=True))
    def get(self):
        return HistoryModel.query.all()
    

@blp.route("/exchanges/history", methods=["GET"])
class HistorySearch(MethodView):
    # This route will return the history of trades based on the search criteria
    @blp.arguments(SearchHistorySchema, location="query")
    def get(self, args):
        exchange_id = request.args.get("exchange_id")
        offset = request.args.get("offset", default=0, type=int)
        limit = request.args.get("limit", default=10, type=int)
        search = request.args.get("search")
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")

        trades = HistoryModel.query

        if exchange_id:
            trades = trades.filter(HistoryModel.exchange_id == exchange_id)

        if search:
            trades = trades.filter(
                or_(
                    (HistoryModel.currency_in.ilike(f"%{search}%")),
                    (HistoryModel.currency_out.ilike(f"%{search}%"))
                )
            )

        if date_from:
            trades = trades.filter(HistoryModel.timestamp >= date_from)

        if date_to:
            trades = trades.filter(HistoryModel.timestamp <= date_to)

        trades = trades.offset(offset).limit(limit).all()
        logging.info(f'The history is searched by criteria')
        return jsonify(HistorySchema(many=True).dump(trades)), 200
    
      