from flask import Flask, request, render_template , jsonify
import os
import data_process

output_dir = 'storage/output/'
original_data_dir = 'storage/original_data/'
preprocessed_data_dir = 'storage/preprocessed_data/'
imgs_dir = 'storage/imgs/'

if(not os.path.exists(output_dir)): os.makedirs(output_dir)
if(not os.path.exists(original_data_dir)): os.makedirs(original_data_dir)
if(not os.path.exists(preprocessed_data_dir)): os.makedirs(preprocessed_data_dir)
if(not os.path.exists(imgs_dir)): os.makedirs(imgs_dir)

app = Flask(__name__,
            template_folder='./static/templates',
            )

# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():   # 将上传的文件保存到"storage\original_data"文件夹下，文件名与上传文件同名，若重名则覆盖
    file = request.files['file']
    global file_path
    file_path = os.path.join(original_data_dir, file.filename)
    file.save(file_path)
    return '后端文件上传成功: ' + file.filename

@app.route('/data_preprocess', methods=['GET'])
def data_preprocess():  # 返回：二维化的数据、Protein值、聚类标签
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "缺少filename参数"}), 400
    file_path = os.path.join(preprocessed_data_dir, filename)
    print('收到文件：'+file_path)
    
    x_umap , Protein , cluster_ids_x = data_process.kmeans(file_path,preprocessed_data_dir)
    
    data = {
        'x_umap': x_umap.tolist(),
        'Protein': Protein.tolist(),
        'cluster_ids_x': cluster_ids_x.tolist(),
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=False,port=5000)