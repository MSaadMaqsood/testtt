from fpdf import FPDF
from datetime import datetime

def pdf_maker(street_name, street_info, violation_date_total, violation_table_data):

    now = datetime.now()
    current_time = now.strftime("%b %d, %Y")
    # street_info = {"street_risk_rate": 5, "green_index": 95, "Asphalt": 40, "Sidewalk": 60,
    #                "Lighting": 71, "Cleanliness": 90, "Afforestation": 95, "Fossils": 92}
    # violation_table_data = [{
    #     "violation_id": 1,
    #     "violation_type_id": 1,
    #     "accurate": 94,
    #     "risk": 5,
    #     "display_img": "1.jpg",
    #     "violation_date": "Sep 29, 2022",
    #     "violation_time": "03:29",
    #     "violation_name": "Asphalt"
    # }]

    pdf = FPDF(orientation='P', unit='pt', format='letter')

    pdf.add_page()

    pdf.set_font(family='Times', style='B', size=24)
    pdf.rect(x=5, y=5, w=601, h=780, style='B')
    pdf.set_font(family='Times', style='', size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(w=0, h=20, txt="Generated On: " + str(current_time), align='R',  ln=1)
    pdf.set_font(family='Times', style='B', size=24)

    pdf.cell(w=0, h=30, txt=str(street_name), align='C', ln=1)
    pdf.set_font(family='Times', style='B', size=18)
    pdf.set_text_color(93,93,93)

    pdf.cell(w=0, h=40, txt="  Violations", align='C', ln=1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_text_color(255, 0, 0)
    pdf.set_font(family='Times', style='B', size=14)
    txt1 = str(street_info.get("street_risk_rate"))
    pdf.cell(w=0, h=15, txt='Risk Rate:   ' + txt1 + "%", align='C', ln=1)
    pdf.set_font(family='Times', size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family='Times', style='B', size=15)
    pdf.cell(w=0, h=50, txt='Street Status:', ln=1)
    pdf.set_font(family='Times', style='I', size=12)
    pdf.cell(w=0, h=15, txt='Asphalt Health:  ', ln=0)

    if street_info.get("Asphalt") < 50:
        pdf.set_fill_color(255, 0, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=110, h=15, txt=str(street_info.get("Asphalt")) + "%   ", border=0, ln=2, align='L', fill=1)
    elif street_info.get("Asphalt") < 70:
        pdf.set_fill_color(255, 165, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=210, h=15, txt=str(street_info.get("Asphalt")) + "%   ", border=0, ln=1, align='L', fill=1)
    else:
        pdf.set_fill_color(0, 128, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=310, h=15, txt=str(street_info.get("Asphalt")) + "%   ", border=0, ln=1, align='L', fill=1)

    pdf.ln(15)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family='Times', style='I', size=12)
    pdf.cell(w=0, h=15, txt='Sidewalk  Health:  ', align='L', ln=0)

    if street_info.get("Sidewalk") < 50:
        pdf.set_fill_color(255, 0, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=110, h=15, txt=str(street_info.get("Sidewalk")) + "%   ", border=0, ln=2, align='L', fill=1)
    elif street_info.get("Sidewalk") < 70:
        pdf.set_fill_color(255, 165, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=210, h=15, txt=str(street_info.get("Sidewalk")) + "%   ", border=0, ln=2, align='L', fill=1)
    else:
        pdf.set_fill_color(0, 128, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=310, h=15, txt=str(street_info.get("Sidewalk")) + "%   ", border=0, ln=2, align='L', fill=1)

    pdf.ln(15)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family='Times', style='I', size=12)
    pdf.cell(w=0, h=15, txt='Lighting  Health:  ', align='L', ln=0)

    if street_info.get("Lighting") < 50:
        pdf.set_fill_color(255, 0, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=110, h=15, txt=str(street_info.get("Lighting")) + "%   ", border=0, ln=2, align='L', fill=1)
    elif street_info.get("Lighting") < 70:
        pdf.set_fill_color(255, 165, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=210, h=15, txt=str(street_info.get("Lighting")) + "%   ", border=0, ln=2, align='L', fill=1)
    else:
        pdf.set_fill_color(0, 128, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=310, h=15, txt=str(street_info.get("Lighting")) + "%   ", border=0, ln=2, align='L', fill=1)

    pdf.ln(15)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family='Times', style='I', size=12)
    pdf.cell(w=0, h=15, txt='Cleanliness  Health:  ', align='L', ln=0)

    if street_info.get("Cleanliness") < 50:
        pdf.set_fill_color(255, 0, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=110, h=15, txt=str(street_info.get("Cleanliness")) + "%   ", border=0, ln=2, align='L', fill=1)
    elif street_info.get("Cleanliness") < 70:
        pdf.set_fill_color(255, 165, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=210, h=15, txt=str(street_info.get("Cleanliness")) + "%   ", border=0, ln=2, align='L', fill=1)
    else:
        pdf.set_fill_color(0, 128, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=310, h=15, txt=str(street_info.get("Cleanliness")) + "%   ", border=0, ln=2, align='L', fill=1)

    pdf.ln(15)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family='Times', style='I', size=12)
    pdf.cell(w=0, h=15, txt='Afforestation   Health:  ', align='L', ln=0)

    if street_info.get("Afforestation") < 50:
        pdf.set_fill_color(255, 0, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=110, h=15, txt=str(street_info.get("Afforestation")) + "%   ", border=0, ln=2, align='L', fill=1)
    elif street_info.get("Afforestation") < 75:
        pdf.set_fill_color(255, 165, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=210, h=15, txt=str(street_info.get("Afforestation")) + "%   ", border=0, ln=2, align='L', fill=1)
    else:
        pdf.set_fill_color(0, 128, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=310, h=15, txt=str(street_info.get("Afforestation")) + "%   ", border=0, ln=2, align='L', fill=1)

    pdf.ln(15)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family='Times', style='I', size=12)
    pdf.cell(w=0, h=15, txt='Fossils   Health:  ', align='L', ln=0)

    if street_info.get("Fossils") < 50:
        pdf.set_fill_color(255, 0, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=110, h=15, txt=str(street_info.get("Fossils")) + "%   ", border=0, ln=2, align='L', fill=1)
    elif street_info.get("Fossils") < 70:
        pdf.set_fill_color(255, 165, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=210, h=15, txt=str(street_info.get("Fossils")) + "%   ", border=0, ln=2, align='L', fill=1)
    else:
        pdf.set_fill_color(0, 128, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=310, h=15, txt=str(street_info.get("Fossils")) + "%   ", border=0, ln=2, align='L', fill=1)

    pdf.ln(25)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family='Times', style='B', size=14)
    pdf.cell(w=0, h=15, txt='Green Index:  ', align='L', ln=0)

    if street_info.get("green_index") < 50:
        pdf.set_fill_color(255, 0, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=200, h=15, txt=str(street_info.get("green_index")) + "%   ", border=0, ln=0, align='L', fill=1)
        pdf.set_fill_color(255, 165, 0)
        pdf.cell(w=45, h=15, txt="", border=1, ln=1, align='L', fill=1)
    elif street_info.get("green_index") < 70:
        pdf.set_fill_color(255, 165, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=260, h=15, txt=str(street_info.get("green_index")) + "%   ", border=0, ln=0, align='L', fill=1)
        pdf.set_fill_color(255, 165, 0)
        pdf.cell(w=45, h=15, txt="", border=1, ln=1, align='L', fill=1)
    else:
        pdf.set_fill_color(0, 128, 0)
        pdf.cell(-440)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=360, h=15, txt=str(street_info.get("green_index")) + "%   ", border=0, ln=0, align='L', fill=1)
        pdf.set_fill_color(255, 165, 0)
        pdf.cell(w=45, h=15, txt="", border=0, ln=1, align='L', fill=1)

    pdf.set_font(family='Times', style='B', size=15)
    pdf.ln(25)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(w=0, h=15, txt='Cases Details:', ln=1)
    pdf.set_font(family='Times', style='B', size=10)
    pdf.cell(w=0, h=40, txt='Total Violations: '+str(len(violation_table_data)), ln=0)
    pdf.cell(-130)
    pdf.cell(w=0, h=40, txt="Date: " + str(violation_date_total), ln=1)

    for i in range(len(violation_table_data)):
        pdf.set_text_color(0, 0, 0)
        violation_id: str | int | None = violation_table_data[i].get("violation_id")
        violation_date = violation_table_data[i].get("violation_date")
        violation_time = violation_table_data[i].get("violation_time")
        violation_name = violation_table_data[i].get("violation_name")
        accurate = violation_table_data[i].get("accurate")
        risk = violation_table_data[i].get("risk")
        pdf.set_fill_color(255, 255, 255)
        pdf.set_font(family='Courier', style='B', size=10)
        pdf.cell(w=50, h=15, txt=str(violation_id), border=1, ln=0, align='C', fill=1)
        pdf.cell(20)
        pdf.set_font(family='times', size=9)
        pdf.cell(w=140, h=15, txt=str(violation_date) + " at " + str(violation_time), border=1, ln=0, align='C', fill=1)
        pdf.cell(20)
        pdf.cell(w=90, h=15, txt=str(violation_name), border=1, ln=0, align='C', fill=1)
        pdf.cell(20)
        pdf.cell(w=90, h=15, txt="Accurate: " + str(accurate) + "%", border=1, ln=0, align='C', fill=1)
        pdf.cell(20)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(w=90, h=15, txt="Risk: " + str(risk) + "%", border=1, ln=1, align='C', fill=1)
        to_page_2 = pdf.add_link()
        pdf.cell(20)
        pdf.set_text_color(0, 0, 255)
        pdf.cell(70, 15, 'Go to image', border=1, ln=1, align='C', fill=1, link=to_page_2)
        pdf.ln(15)

    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family='Times', style='B', size=12)
    pdf.cell(100)
    ##Add for loop here for list of images
    for i in range(len(violation_table_data)):
        violation_id: str | int | None = violation_table_data[i].get("violation_id")
        pdf.cell(w=0, h=15, txt='Violation # ' + str(violation_id) + ': ', align='L', ln=0)
        pdf.cell(-350)
        ##to_page_2 = pdf.add_link()
        pdf.set_link(to_page_2, page=2)
        pdf.image(w=200, h=100, type='png', link="to_page_2",
              name='https://psprop.net/wp-content/uploads/2012/02/HOA-Trash-Can-Violation.png')
    pdf_name = street_name+"_"+str(violation_date_total)+"_"+datetime.now().strftime("%b-%d-%Y_%H:%M")+".pdf"
    pdf.output("1.pdf")
    print("xzcxzcxzcxz")
    return pdf_name


street_info = {
        "street_risk_rate": 0,
        "green_index": 0,
        "Asphalt": 100,
        "Sidewalk": 100,
        "Lighting": 100,
        "Cleanliness": 100,
        "Afforestation": 100,
        "Fossils": 100
    }
violations = [
      {
        "accurate": "95",
        "display_img": "1.jpg",
        "risk": "3",
        "violation_date": "Oct 06, 2022",
        "violation_id": 1,
        "violation_name": "Minor Asphalt",
        "violation_time": "04:03",
        "violation_type_id": "1"
      },
      {
        "accurate": "94",
        "display_img": "1.jpg",
        "risk": "11",
        "violation_date": "Oct 06, 2022",
        "violation_id": 2,
        "violation_name": "Sidewalk",
        "violation_time": "04:05",
        "violation_type_id": "2"
      },
      {
        "accurate": "76",
        "display_img": "1.jpg",
        "risk": "5",
        "violation_date": "Oct 06, 2022",
        "violation_id": 3,
        "violation_name": "Minor Asphalt",
        "violation_time": "22:34",
        "violation_type_id": "1"
      },
      {
        "accurate": "82",
        "display_img": "1.jpg",
        "risk": "7",
        "violation_date": "Oct 06, 2022",
        "violation_id": 6,
        "violation_name": "Lighting",
        "violation_time": "10:44",
        "violation_type_id": "3"
      },
      {
        "accurate": "111",
        "display_img": "1.jpg",
        "risk": "11",
        "violation_date": "Oct 06, 2022",
        "violation_id": 8,
        "violation_name": "Minor Asphalt",
        "violation_time": "03:41",
        "violation_type_id": "1"
      },
      {
        "accurate": "111",
        "display_img": "1.jpg",
        "risk": "11",
        "violation_date": "Oct 06, 2022",
        "violation_id": 9,
        "violation_name": "Minor Asphalt",
        "violation_time": "03:41",
        "violation_type_id": "1"
      },
      {
        "accurate": "1",
        "display_img": "1.jpg",
        "risk": "1",
        "violation_date": "Oct 06, 2022",
        "violation_id": 10,
        "violation_name": "Minor Asphalt",
        "violation_time": "04:24",
        "violation_type_id": "1"
      },
      {
        "accurate": "1",
        "display_img": "1.jpg",
        "risk": "1",
        "violation_date": "Oct 06, 2022",
        "violation_id": 11,
        "violation_name": "Minor Asphalt",
        "violation_time": "04:24",
        "violation_type_id": "1"
      },
      {
        "accurate": "1",
        "display_img": "1.jpg",
        "risk": "1",
        "violation_date": "Oct 06, 2022",
        "violation_id": 12,
        "violation_name": "Minor Asphalt",
        "violation_time": "04:24",
        "violation_type_id": "1"
      },
      {
        "accurate": "1",
        "display_img": "1.jpg",
        "risk": "1",
        "violation_date": "Oct 06, 2022",
        "violation_id": 13,
        "violation_name": "Minor Asphalt",
        "violation_time": "04:24",
        "violation_type_id": "1"
      },
      {
        "accurate": "1",
        "display_img": "1.jpg",
        "risk": "1",
        "violation_date": "Oct 06, 2022",
        "violation_id": 14,
        "violation_name": "Minor Asphalt",
        "violation_time": "04:24",
        "violation_type_id": "1"
      }
    ]


pdf_maker("XYZZZZZZZZZZZZZZZZZZ", street_info, "Oct 06, 2022", violations)