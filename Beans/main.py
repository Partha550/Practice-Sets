from flask import Flask, request, render_template, url_for
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def Home():
    if request.method == 'POST':
        length = float(request.form["beamlength"])
        sup_1 = float(request.form["first_support"])
        sup_2 = float(request.form["second_support"])
        support = (sup_1, sup_2)
        print(length, support)
    else:
        return render_template('index.html')

@app.route('/loads-&-moments', methods=['POST', 'GET'])
def add_loads():
    if request.method == 'POST':
        input_boxes, force_ele = ['pl_pos', 'pl_mag', 'udl_spos', 'udl_epos', 'udl_mag', 
            'uvl_spos', 'uvl_epos', 'uvl_smag', 'uvl_emag', 'pm_pos', 'pm_mag', 'udm_spos', 
            'udm_epos', 'udm_mag', 'uvm_spos', 'uvm_epos', 'uvm_smag', 'uvm_emag'], []
        for box in input_boxes:
            value = float(request.form.get(box, False))
            if value != 0:
                force_ele.append(value)
        print(force_ele)
    return render_template('add_loads_and_moments.html')

if __name__ == '__main__':
    app.run(debug=True, host="192.168.0.107", port="8080")
    