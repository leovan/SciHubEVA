from tempfile import TemporaryFile

from flask import Flask, Response, make_response, request, send_file

from scihub_eva.utils.path_utils import *

app = Flask(__name__)


@app.route('/', methods=['POST'])
def pdf_url_query() -> tuple[Response, int]:
    post_request = request.form.get('request')
    if post_request:
        return pdf_url_response(request.host_url, post_request), 200
    else:
        return make_response('UNKNOWN'), 400


def pdf_url_response(host_url: str, post_request: str) -> Response:
    return make_response(f'''
    <html>
      <body>
        <div id="article">
          <embed
            type="application/pdf"
            src="{host_url}{post_request}.pdf"
            id="pdf">
          </embed>
        </div>
      </body>
    </html>
    ''')


@app.route('/<pdf>', methods=['GET'])
def pdf_query(pdf: str) -> Response:
    if pdf.find('captcha') != -1:
        return captcha_response(request.host_url, pdf)

    return send_file(TemporaryFile(), mimetype='application/pdf', download_name=pdf)


@app.route('/<pdf>', methods=['POST'])
def pdf_captcha_query(pdf: str) -> Response:
    post_answer = request.form.get('answer', '')

    if post_answer.lower() != 'moment':
        return make_response('WRONG CAPTCHA!')
    else:
        return send_file(TemporaryFile(), mimetype='application/pdf', download_name=pdf)


def captcha_response(host_url: str, pdf: str) -> Response:
    return make_response(f'''
    <html>
      <body>
        <img id="captcha" src="{host_url}captcha-moment.png" />
        <input name="id" value="{pdf.split('.')[0]}"/>
      </body>
    </html>
    ''')


@app.route('/captcha-moment.png', methods=['GET'])
def captcha_img() -> Response:
    return send_file(
        (IMAGES_DIR / 'captcha-moment.png').resolve().as_posix(), mimetype='image/png'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
