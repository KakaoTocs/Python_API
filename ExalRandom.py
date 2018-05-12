import openpyxl
import os
import sys
import io
import random

# 출력시 인코딩
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')

array = []

# 현재 경로
subdir = os.path.dirname(os.path.abspath(__file__))


# 엑셀 파일 열기
wb = openpyxl.load_workbook(subdir + '\studentList.xlsx')
ws = wb.active

# 이름 읽어서 배열에 추가
for r in ws.rows:
    array.append(r[1].value)

# 제외 대상
array.remove("김진우")
array.remove("금강현")
array.remove("손제욱")

# 슦아라
random.shuffle(array)

print('1팀: ', array[0], array[1], array[2])
print('2팀: ', array[3], array[4])
print('3팀: ', array[5], array[6])

wb.close()
