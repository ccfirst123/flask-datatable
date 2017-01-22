from flask import request
from app import db
from sqlalchemy import or_
from sqlalchemy.sql import func


class DataTable:
    """
    jquery datatable need to enable server-side processing when load large number of records.
    So some operations must define by ourselves, such as paging, filtering, ordering.
    the class try to make it easier.

    request: come from jquery datatable plugin
    model_object: Model (database table) for query
    """
    def __init__(self, request, model_object):
        self.request = request
        self.model_object = model_object
        self.cardinality = 0
        self.cardinality_filtered = 0
        self.results = None
        self.run_query()

    def output_result(self):
        output = {}
        #sEcho, iTotalRecords... used by datatable, new version of jquery dt use other name instead
        #make sure the name is correct
        output["sEcho"] = int(self.request.args.get('sEcho'))
        output["iTotalRecords"] = self.cardinality
        output["iTotalDisplayRecords"] = self.cardinality_filtered
        output["aaData"] = self.results
        return output

    def run_query(self):
        #select count()
        # method 1: convert to subquery, makes the query very slow
        #self.cardinality = self.model_object.query.count()

        #method 2: use func_, avoid subquery
        self.cardinality = db.session.query(func.count(self.model_object.id)).first()

        #get columns name from request
        column_count = int(self.request.args.get('iColumns'))
        column_list = []
        for i in range(column_count):
            column_name = self.request.args.get('mDataProp_%d' % i)
            column_list.append(column_name)

        #filtering
        search_value = self.request.args.get('sSearch')
        filter_list = []
        if search_value != "":
            for col in column_list:
                column_type = getattr(getattr(self.model_object, col), 'type')
                #col_name like '%search_value%', datatime-type column will raise exception in mysql
                if not isinstance(column_type, db.DateTime):
                    filter_list.append(getattr(self.model_object, col).like("%" + search_value + "%"))

        #sorting
        order_column_index = int(self.request.args.get('iSortCol_0'))
        order_column = getattr(self.model_object, column_list[order_column_index])
        order_dir = self.request.args.get('sSortDir_0')
        order_object = getattr(order_column, order_dir)()

        #paging
        start = self.request.args.get('iDisplayStart', 0, type=int)
        length = self.request.args.get('iDisplayLength', 1, type=int)

        #method 1: use flask pagination, easy, but pagination.total with bring subquery which make query slow
        #page = start / length + 1
        #if search_value != "":
        #   pagination = self.model_object.query.filter(or_(*filter_list)).order_by(order_object).paginate(
        #           page, per_page=length, error_out=False)
        #else:
        #   pagination = self.model_object.query.order_by(order_object).paginate(
        #           page, per_page=length, error_out=False)
        #items = pagination.items
        #self.cardinality_filter = pagination.total

        #method 2: use sqlalchemy offset, limit, avoid subquery
        items = self.model_object.query.filter(or_(*filter_list)).order_by(order_object) \
                    .offset(start).limit(length).all()
        self.cardinality_filtered = db.session.query(func.count(self.model_object.id)) \
                    .filter(or_(*filter_list)).order_by(None).first()
        self.results = [i.to_json for i in items]

