import sqlite3


class MenuItem: #메뉴
    def __init__(self, pno, name, imagePath, price):
        self.pno = pno #product number 메뉴번호
        self.name = name #메뉴 이름
        self.imagePath = imagePath #이미지 경로
        self.price = price #메뉴 가격
"""
class MemberItem: #회원정보
    def __init__(self, id, name, money):
        self.id = id #회원 id
        self.name = name #회원 이름
        self.money = money #유저 머니
"""

class Database: #DB(임시로 클래스로 정의) -> DB.db로 연결
    def __init__(self):
        pass
        #self.__memberList = {1234: MemberItem(1234, '철수', 100000), 5678: MemberItem(5678, '영이', 4000)} #

    def getMenuList(self): #menu list 불러오기
        self.conn = sqlite3.connect("DB.db")
        self.cur = self.conn.cursor()
        self.__menuList = []
        self.cur.execute("SELECT * FROM menuInfo")
        menuDatas = self.cur.fetchall()
        for menuData in menuDatas:
            self.__menuList.append(MenuItem(menuData[0], menuData[1], menuData[2], menuData[3]))
        self.conn.close()
        return self.__menuList

    def getUserChargedMoney(self, userId):
        self.conn = sqlite3.connect("DB.db")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM customerInfo WHERE num='%d'" % userId)
        result = self.cur.fetchone()

        if result is None:
            print("Invalid User")
            self.conn.close()
            return -1
        else:
            self.conn.close()
            return result[2]

    def updateUserMoney(self,userId,updatedMoney):
        self.conn = sqlite3.connect("DB.db")
        self.cur = self.conn.cursor()
        self.cur.execute("UPDATE customerInfo SET chargedMoney='%d' WHERE num='%d'" % (updatedMoney, userId))
        self.conn.commit()
        self.conn.close()

"""
    def getMemberList(self): # member list 불러오기
        return self.__memberList
"""


class UIMaker: # UI 라이브러리 사용
    def printMenu(self, menuList):
        for item in menuList: #menu list = (pno, name, price)
            print("번호: %d 메뉴: %s 가격: %d" %(item.pno, item.name, item.price))
            #print()
        print("번호: 0, 결제하기") # 결제하기 버튼
        print()

    def printPayConfirm(self, totalPrice, chargedMoney):
        print("총 결제금액: %d 회원님의 잔액: %d" % (totalPrice, chargedMoney)) #user.money-> chargedMoney
        #print()
        answer = input("결제하시겠습니다? (Y/N)")
        if answer == 'Y' or answer == 'y':
            return True
        else:
            return False

    def printFinish(self):
        print("결제가 완료되었습니다.")
        print()

    def printFailed(self):
        print("잔액이 부족합니다.")
        print()

    def printRecharge(self):
        answer = input("충전하시겠습니까? (Y/N)")
        if answer == 'Y' or answer == 'y':
            return True
        else:
            return False

    def makeError(self):
        print("menu list가 존재하지 않습니다.")


class OrderStorage:
    def saveCustomerOrder(self, pnoList, menuList):
        self.pnoList = pnoList #order storage에 주문서 저장
        sum = 0

        for menu in pnoList:
            for item in menuList:
                if menu == item.pno: #사용자가 선택한 메뉴가 메뉴 리스트에 있다면
                    sum += item.price #총 계산금액 계산
                    break

        self.totalPrice = sum


    def loadCustomerOrder(self): #order storage에 저장된 주문서를 반환
        return self.pnoList


class Pay:
    def doCheckPayment(self, totalPrice, chargedMoney):
        if totalPrice <= chargedMoney: #유저 머니가 총 계산금액보다 크다면 user.money-> chargedMoney
            return True
        else: #잔액이 부족
            return False

    def payment(self,totalPrice, chargedMoney):
        if self.doCheckPayment(totalPrice, chargedMoney) == True: #유저머니가 충분하다면 user.money-> chargedMoney
            chargedMoney -= totalPrice #결제(유저머니  차감) user.money-> chargedMoney
            return chargedMoney # return값 수정

'''
class InterfacePage:
'''

class Controller:
    def __init__(self):
        self.DB = Database()
        self.UIM = UIMaker()
        self.OS = OrderStorage()
        self.pay = Pay() # (instance를 private으로...)

    def getMenuList(self): # DB에서 메뉴 리스트 불러오기
        menuList = self.DB.getMenuList()
        return menuList

    #def getMemberList(self):
        #memberList = self.DB.getMemberList()
        #return memberList

    def getUserChargedMoney(self, userId):
        userChargedMoney = self.DB.getUserChargedMoney(userId)
        return userChargedMoney

    def run(self):
        while(True):
            menuList = self.getMenuList()
            self.UIM.printMenu(menuList) #UI로 메뉴 출력

            #  ** make order **
            #memberList = self.getMemberList()  # DB에서 회원정보 불러오기
            orderNumber = [] #사용자가 주문한 메뉴들의 번호를 저장할 리스트
            while(True):
                num = int(input("메뉴를 입력하세요. ")) #임시로 사용자에게 번호를 입력받아 메뉴를 선택받는 형식(1~3번)
                if num != 0:
                    orderNumber.append(num)
                else: #0번 = 결제하기
                    break
            self.OS.saveCustomerOrder(orderNumber, menuList) #order storage에 사용자가 주문한 메뉴의 번호 리스트(number)와 메뉴정보(가격 계산용) 저장

            #user = None
            while(True):
                print()
                id = int(input("id를 입력하세요. ")) # UIMaker (이 부분은 별도의 usecase가 있으므로 임의로)
                userChargedMoney = self.getUserChargedMoney(id)
                if userChargedMoney >= 0:
                    break
                #if id in memberList: # 사용자가 입력한 id가 회원정보에 있다면
                    #user = memberList[id] # user 변수에 회원정보(id, 이름, 머니) 저장
                    #break
                '''
                else: #만약 등록된 id가 아니라면?
                    id = int(input("다시 id를 입력하세요. "))
                '''

            #  *. 결제하기
            totalPrice = self.OS.totalPrice
            #payResult =
            if self.pay.doCheckPayment(totalPrice, userChargedMoney) == True: #잔액이 존재
                #yn =
                if self.UIM.printPayConfirm(totalPrice, userChargedMoney) == True: #결제진행을 원한다면
                    updatedMoney = self.pay.payment(totalPrice, userChargedMoney)
                    if updatedMoney >= 0:
                        self.DB.updateUserMoney(id, updatedMoney)
                        self.UIM.printFinish()

                    else: #결제실패(잔액부족)
                        self.UIM.printFailed()
                        '''
                        if self.UIM.printRecharge() == True:
                            self.pay.
                        else: # 결제 취소
                        '''

                else: #잔액이 존재하지만 결제는 원하지 않는 경우.
                    #(ex. 갑자기 결제하기 싫어졌을 때 or 메뉴를 변경하고 싶을 때 or
                    continue  # 새 user?
                    # 이전 창으로 이동
            else:
                self.UIM.printFailed()
                self.UIM.printRecharge()
                #continue # 잔액부족. 결제실패사유
                # 충전금액이 없을 때 창만 띄우면 되는 정도. 충전안내창. 충전: 임의적으로 user.money금액 더하고 pay함수 호출. NO: 종료


if __name__ == "__main__":
    controller = Controller()
    controller.run()



