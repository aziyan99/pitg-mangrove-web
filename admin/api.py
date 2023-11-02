from flask import Blueprint
from flask_restx import Api, Resource, fields, reqparse
from werkzeug.utils import secure_filename
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import tensorflow as tf

from admin.mangrove import get_mangrove_by_dataid

class_labels = {
    "Avicennia alba": 0,
    "Bruguiera cylindrica": 1,
    "Bruguiera gymnorrhiza": 2,
    "Lumnitzera littorea": 3,
    "Rhizophora apiculata": 4,
    "Rhizophora mucronata": 5,
    "Sonneratia alba": 6,
    "Xylocarpus granatum": 7,
}


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(
    bp,
    version="1.0",
    title="Mangrove API",
    description="API for Mangrove Prediction",
    base_url=f"/api",
)

ns1 = api.namespace("v1", description="V1 of mangrove predict")

upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    "file", location="files", type=reqparse.FileStorage, required=True
)

marshal_response = api.model(
    "Predict",
    {
        "title": fields.String(
            description="Title of the mangrove", default="Mangrove A"
        ),
        "data_id": fields.Integer(
            description="Prediction ID of the mangrove", default=1
        ),
        "banner_path": fields.String(
            description="Banner path of the mangrove",
            default="https://foo.bar/image.jpg",
        ),
        "body": fields.String(
            description="Body of the mangrove", default="Lorem ipsum dolor sit amet ..."
        ),
        "created_at": fields.DateTime(description="Creation timestamp of the mangrove"),
    },
)

error_response_model_400 = api.model(
    "Error400",
    {
        "message": fields.String(description="Bad Request error message"),
    },
)

error_response_model_500 = api.model(
    "Error500",
    {
        "message": fields.String(description="Internal Server Error message"),
    },
)

CURRENT_DIR = os.getcwd()
MODEL_NAME = "202310221831.h5"


@ns1.route("/predict", endpoint="predict")
@api.expect(upload_parser)
class Predict(Resource):
    @api.marshal_with(marshal_response)
    @api.response(400, "Bad Request", error_response_model_400)
    @api.response(500, "Bad Request", error_response_model_500)
    def post(self):
        # fields_mask = request.headers.get("X-Fields")  # Don't know it is really used

        args = upload_parser.parse_args()
        uploaded_file = args["file"]

        try:
            img = Image.open(uploaded_file)
            img.verify()  # Verifying the image data
            img.close()
        except Exception as e:
            api.abort(400, "Invalid image file")

        filename = secure_filename(uploaded_file.filename)
        img = Image.open(uploaded_file)
        img.save(os.path.join(CURRENT_DIR, "admin", "static", filename))

        pred_image = image.load_img(
            os.path.join(CURRENT_DIR, "admin", "static", filename),
            target_size=(150, 150),
        )

        x = image.img_to_array(pred_image)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0

        model = load_model(os.path.join(CURRENT_DIR, "admin", "static", MODEL_NAME))
        prediction = model.predict(x)
        predicted_class_idx = np.argmax(prediction, axis=1)[0]
        predicted_class_name = [
            k for k, v in class_labels.items() if v == predicted_class_idx
        ][0]

        print(predicted_class_idx)

        os.remove(os.path.join(CURRENT_DIR, "admin", "static", filename))

        predicted_magrove = get_mangrove_by_dataid(int(predicted_class_idx))
        magrove = {
            "title": predicted_magrove["title"],
            "data_id": predicted_magrove["data_id"],
            "banner_path": predicted_magrove["banner_path"],
            "body": predicted_magrove["body"],
            "created_at": predicted_magrove["created_at"],
        }

        return magrove, 200
