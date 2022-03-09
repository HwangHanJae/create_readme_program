from bs4 import BeautifulSoup
import requests
import sys

def find_title():
  title_list  = soup.find_all("span", attrs={"id":"problem_title"})
  for title in title_list:
    problem_title = title.get_text()
  return problem_title

def find_problem_number():
  number_list = soup.find_all('span', attrs={"class" : "printable"})
  for number in number_list:
    number_title = number.get_text().replace('-', '').strip()
  return number_title

def find_problem_description():
  problems = soup.find_all('div', attrs={'id' : 'problem_description'})[0]
  problems = str(problems).replace("</p>","")
  problems = problems.replace("</div>","")
  problems = problems.replace('<div class="problem-text" id="problem_description">\n', "")
  problems = problems.replace("\n", "\n\n")
  problems = problems.split("<p>")
  problem_result = ""
  for i in range(1, len(problems)):
    if "img"  in problems[i]:
      problem_result += "\n\n"
    else:
      problem_result += problems[i]
  return problem_result

def find_problem_input():
  input_data = soup.find_all('div', attrs = {"id":"problem_input"})[0]
  input_data = str(input_data).replace('<div class="problem-text" id="problem_input">\n', "")
  input_data = input_data.replace("</p>",'')
  input_data = input_data.replace("</div>","")
  input_data = input_data.replace("\n",'\n\n')
  input_data = input_data.split("<p>")
  input_result = ''
  for i in range(1, len(input_data)):
    input_result += input_data[i]
  return input_result

def find_problem_output():
  output_data = soup.find_all('div', attrs = {"id" : "problem_output"})
  output_result = ''
  for data in output_data:
    output_result += data.get_text()
  return output_result

try :
  #백준 사이트의 정보를 받을때 403 에러가 나오는데
  #이를 해결하기 위하여 headers를 추가하여 해결
  link = sys.stdin.readline().rstrip()
  headers = {'User-Agent':'Chrome/66.0.3359.181'}
  webpage = requests.get(link, headers=headers)
  soup = BeautifulSoup(webpage.content, 'html.parser')

  #file 만들기
  file_name = 'readme.md'
  f = open(file_name, 'w', encoding="UTF-8")

  #타이틀 찾기
  problem_title = find_title()
  #문제 번호찾기
  number_title = find_problem_number()
  #타이틀 설정
  title = "<h1>{0} - {1}</h1>\n\n".format(problem_title, number_title)
  f.write(title)

  #문제 내용찾기
  problem_result = find_problem_description()
  #문제 설정
  problem_title = "<h2>{}</h2>\n\n".format("문제")
  f.write(problem_title)
  f.write(problem_result)

  #입력 내용 찾기
  input_result = find_problem_input()
  #입력 설정
  input_title = "<h2>{}</h2>\n\n".format("입력")
  f.write(input_title)
  f.write(input_result)

  #출력 내용 찾기
  output_result = find_problem_output()
  #출력 설정
  output_title = "<h2>{}</h2>\n".format("출력")
  f.write(output_title)
  f.write(output_result+"\n")

  #출처 설정
  source_title = "<h2>{}</h2>\n\n".format("출처")
  f.write(source_title)

  #출처 내용 설정
  defalut = "[백준 {}]({})".format(number_title.replace('번',''), link)
  f.write(defalut)
  f.close()
  print("readme 완성")
except:
  print("에러 발생")
