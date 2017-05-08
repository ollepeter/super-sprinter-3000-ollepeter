import os
import csv
from flask import Flask, request, render_template, redirect

app = Flask(__name__)
csv_filename = "data_table.csv"
full_path = os.path.realpath(__file__)
csv_file = "/".join((os.path.split(full_path)[0], csv_filename))

HEADER_ROW = ["ID",
              "Story Title",
              "User Story",
              "Acceptance Criteria",
              "Business Value",
              "Estimation",
              "Status",
              ]


def read_csv():
    '''Read csv file and make a create the data table (list of lists)'''
    story_table = []
    with open(csv_file, mode='r', encoding='utf - 8') as f:
        content = csv.reader(f, delimiter=',')
        for row in content:
            story_table.append(row)
    return story_table


def write_csv(story_table):
    '''Write the datatable into csv file csv'''
    with open(csv_file, mode='w', encoding='utf - 8') as f:
        datawriter = csv.writer(f, delimiter=',')
        for row in story_table:
            datawriter.writerow(row)


def get_new_id():
    '''Generates new unique ID number based on the existing data table'''
    story_table = read_csv()
    sorted_ids = sorted([int(row[0]) for row in story_table])
    story_id = 0
    if len(sorted_ids) == 0:
        story_id = 1
    else:
        for i in range(1, len(sorted_ids)):
            if int(sorted_ids[i]) - int(sorted_ids[i - 1]) != 1:
                story_id = str(i + 1)
                return story_id
        story_id = str(max(sorted_ids) + 1)
    return story_id


@app.route('/', methods=['GET'])
@app.route('/list', methods=['GET'])
def show_list():
    '''Render the StoryTable'''
    story_table = read_csv()
    story_table = sorted(story_table, key=lambda story_id: int(story_id[0]))
    return render_template('list.html', story_table=story_table, HEADER_ROW=HEADER_ROW)


@app.route('/story', methods=['GET'])
@app.route('/story/<int:story_id>', methods=['GET'])
def story(story_id=False):
    '''Renders the "form.html" with the previous values to update Story Table or 
    without valuse to create a new row in the StoryTable'''
    if story_id:
        story_table = read_csv()
        story_table = sorted(story_table, key=lambda story_id: int(story_id[0]))
        index_list = [int(i[0]) for i in story_table]
        row_index = index_list.index(story_id)
        row = story_table[row_index]
        story_title = row[1]
        user_story = row[2]
        acceptance_criteria = row[3]
        business_value = row[4]
        estimation = row[5]
        status = row[6]
        return render_template('form.html',
                               process='update',
                               form_title='Edit Story',
                               story_id=story_id,
                               story_title=story_title,
                               user_story=user_story,
                               acceptance_criteria=acceptance_criteria,
                               business_value=business_value,
                               estimation=estimation,
                               status=status,
                               form_button='Update',
                               )
    else:
        return render_template('form.html',
                               process='create',
                               # story_title='None',
                               form_title='Add new Story',
                               form_button='Create',
                               )


@app.route('/delete/<int:story_id>', methods=['GET'])
def delete(story_id):
    '''Delete the row from StoryTable according to ID number'''
    story_table = read_csv()
    story_table = sorted(story_table, key=lambda story_id: int(story_id[0]))
    index_list = [int(i[0]) for i in story_table]
    row_index = index_list.index(story_id)
    del story_table[row_index]
    write_csv(story_table)
    return redirect('/list')


@app.route('/story/create/', methods=['POST'])
def creat():
    """Update StoryTable with a new row"""
    story_id = get_new_id()
    form_dict = dict(request.form)
    new_row = [story_id,
               form_dict['story_title'][0],
               form_dict['user_story'][0],
               form_dict['acceptance_criteria'][0],
               form_dict['business_value'][0],
               form_dict['estimation'][0],
               form_dict['status'][0],
               ]
    story_table = read_csv()
    story_table.append(new_row)
    write_csv(story_table)
    return redirect('/list')


@app.route('/story/update/<int:story_id>', methods=['POST'])
def update(story_id):
    """Update StoryTable with an updated row"""
    story_table = read_csv()
    story_table = sorted(story_table, key=lambda story_id: int(story_id[0]))
    index_list = [int(i[0]) for i in story_table]
    row_index = index_list.index(story_id)
    row = story_table[row_index]
    row[1] = str(request.form['story_title'])
    row[2] = str(request.form['user_story'])
    row[3] = str(request.form['acceptance_criteria'])
    row[4] = str(request.form['business_value'])
    row[5] = str(request.form['estimation'])
    row[6] = str(request.form['status'])
    story_table[row_index] = row
    story_table = sorted(story_table, key=lambda story_id: int(story_id[0]))
    write_csv(story_table)
    return redirect('/list')


if __name__ == '__main__':
    app.run(debug=True)
