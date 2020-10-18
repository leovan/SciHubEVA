# -*- coding: utf-8 -*-

from tempfile import TemporaryFile
from flask import Flask, request, send_file

from scihub_eva.utils.path_utils import *


app = Flask(__name__)


@app.route('/', methods=['POST'])
def pdf_url_query():
    post_request = request.form.get('request')
    if post_request:
        return pdf_url_response(request.host_url, post_request)
    else:
        return 'UNKNOWN', 400


def pdf_url_response(host_url: str, request: str):
    return '''
    <html>
      <body>
        <iframe id="pdf" src="{host_url}{request}.pdf"></iframe>
      </body>
    </html>
    '''.format(host_url=host_url, request=request)


@app.route('/<pdf>', methods=['GET'])
def pdf_query(pdf: str):
    if pdf.find('captcha') != -1:
        return captcha_response(request.host_url, pdf)

    return send_file(TemporaryFile(), mimetype='application/pdf', attachment_filename=pdf)


@app.route('/<pdf>', methods=['POST'])
def pdf_captcha_query(pdf: str):
    post_answer = request.form.get('answer', '')

    if post_answer.lower() != 'moment':
        return 'WRONG CAPTCHA!'
    else:
        return send_file(TemporaryFile(), mimetype='application/pdf', attachment_filename=pdf)


def captcha_response(host_url: str, pdf: str):
    return '''
    <html>
      <body>
        <img id="captcha" src="{host_url}captcha-moment.png" />
        <input name="id" value="{pdf}"/>
      </body>
    </html>
    '''.format(host_url=host_url, pdf=pdf.split('.')[0])


@app.route('/captcha-moment.png', methods=['GET'])
def captcha_img():
    return send_file((IMAGES_DIR / 'captcha-moment.png').resolve().as_posix(), mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
