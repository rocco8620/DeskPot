import sys
import os
import pdfkit

TEMPLATE_FILENAME = 'report_template.html'

if len(sys.argv) != 2:
    print("Creates pdf reports from hack attemps data using a template.")
    print("Usage: python3", sys.argv[0], "<hack_attemp_* folder path>")
    sys.exit()

data_folder_path = sys.argv[1]
images_folder_path = os.path.join(data_folder_path, 'photos')

out_file_name = sys.argv[1].rstrip('/').split('/')[-1] + '.pdf'

# Read the template
try:
    template_data = open(TEMPLATE_FILENAME, 'r').read()    
except IOError as e:
    print("Errore apertura file template.")
    print(str(e))

# Add the images if needed
if '{{intruder_images}}' in template_data:
    # get the images
    intruder_images = [ x for x in os.listdir(images_folder_path) if os.path.isfile(os.path.join(images_folder_path, x)) ]

    # fix list len
    if len(intruder_images) % 2 != 0:
        intruder_images.append(None)


    intruder_images_html = '<table border="0">'
    # this takes the images in groups of two
    for i, j in zip(intruder_images[0::2], intruder_images[1::2]):
        intruder_images_html += '<tr><td>'

        if i is not None:
            intruder_images_html += '<img src="' + os.path.abspath(os.path.join(images_folder_path, i)) + '"></img>'

        intruder_images_html += '</td><td>'

        if j is not None:
            intruder_images_html += '<img src="' + os.path.abspath(os.path.join(images_folder_path, j)) + '"></img>'

        intruder_images_html += '</td></tr>'
        
    intruder_images_html += '</table>'



    # Put the data in the template
    template_data = template_data.replace('{{intruder_images}}', intruder_images_html)

#open('out.html', 'w').write(template_data)


options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
}

# Generate the report
pdfkit.from_string(template_data, out_file_name, options=options)
