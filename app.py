import os

from flask import Flask, render_template, request, jsonify

from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher 

# create flask instance
# app = Flask(__name__)
app = Flask(__name__, static_folder = "static")
#app = Flask(__name__, static_url_path ="",static_folder = "static" )
INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')

# main route
@app.route('/')
def index():
    return render_template('index.html')

# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

# search route 
@app.route('/search', methods=[ 'POST'])
def search():

	if request.method == "POST":

		RESULTS_ARRAY = []

		# get url
		image_url = request.form.get('img')

		try:

			# initialize the image descriptor
			cd = ColorDescriptor((8, 12, 3))

			# load and describe query image 
			from skimage import io
			import cv2 
			query = io.imread(image_url)
			query = (query * 255).astype("uint8")
			(r, g, b) = cv2.split(query)
			query = cv2.merge([b, g, r])
			features = cd.describe(query)

			# perform the search 
			searcher = Searcher(INDEX)
			results = searcher.search(features)

			# loop over results, display score
			for (score, resultID) in results:
				RESULTS_ARRAY.append(
						{"image": str(resultID), "score": str(score)})
			
			# return success
			return jsonify(results=(RESULTS_ARRAY[::-1][:3]))
		
		except:

			# return error 
			jsonify({"sorry":"No results, please try again!"}), 500
			



