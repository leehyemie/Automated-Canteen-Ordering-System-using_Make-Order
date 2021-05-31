import sqlite3
from tkinter import *
from tkinter import messagebox


class MenuItem:  # 메뉴
    def __init__(self, pno, name, imagePath, price):
        self.pno = pno  # product number 메뉴번호
        self.name = name  # 메뉴 이름
        self.imagePath = imagePath  # 이미지 경로
        self.price = price  # 메뉴 가격


class DBConnection:  # DB.db로 연결
    def __init__(self):
        self.conn = sqlite3.connect("DB.db")
        self.cur = self.conn.cursor()
        self.__menuList = []
        self.cur.execute("SELECT * FROM menuInfo")
        menuDatas = self.cur.fetchall()
        for menuData in menuDatas:
            self.__menuList.append(MenuItem(menuData[0], menuData[1], menuData[2], menuData[3]))
        self.conn.close()

    def getMenuList(self):  # menu list 불러오기
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

    def updateUserMoney(self, userId, updatedMoney):
        self.conn = sqlite3.connect("DB.db")
        self.cur = self.conn.cursor()
        self.cur.execute("UPDATE customerInfo SET chargedMoney='%d' WHERE num='%d'" % (updatedMoney, userId))
        self.conn.commit()
        self.conn.close()


class UIMaker:  # tkinter 사용
    def __init__(self):
        self.interface = InterfacePage()

    def printMenu(self, menuList):
        orderNumber = []
        global menuWindow
        menuWindow = Tk()
        menuWindow.title("메뉴 리스트")
        menuWindow.geometry("320x480+300+300")
        menuWindow.resizable(False, False)
        scrollFrame = Frame(menuWindow, width=400, height=430, relief="solid")
        scrollFrame.pack(side="top", expand=True, fill="both")
        scrollCanvas = Canvas(scrollFrame, bg='#FFFFFF', scrollregion=(0, 0, 0, len(menuList) * 117.5))
        scrollbar = Scrollbar(scrollFrame)
        scrollbar.pack(side="right", fill="y")
        scrollbar.config(command=scrollCanvas.yview)
        scrollCanvas.config(yscrollcommand=scrollbar.set)
        scrollCanvas.pack(side=LEFT, expand=True, fill=BOTH)
        scrollFrame = Frame(menuWindow)

        image = []
        for item in menuList:  # menu list = (pno, name, imagePath, price)
            image.append(PhotoImage(file=item.imagePath))
            menuFrame = Frame(scrollFrame, bg='#FFFFFF', relief="solid", bd=1)
            Button(menuFrame, text="담기", width=9, height=7, relief='ridge', bd=2, bg='#fae56e',
                   command=lambda i=item.pno: self.interface.makeOrder(orderNumber, i)).pack(side="right", fill='both')
            Label(menuFrame, text=item.price, width=9, height=7).pack(side="right", fill='both')
            Label(menuFrame, text=item.name, width=9, height=7).pack(side="right", fill='both')
            Label(menuFrame, image=image[item.pno - 1001]).pack(side="left", fill='both')
            menuFrame.pack(side="top", fill='x')
        scrollCanvas.create_window(0, 0, anchor='nw', window=scrollFrame)
        Button(menuWindow, text="결제하기", width=6, height=1, relief='ridge', bd=2,
               command=lambda: self.interface.makeOrder(orderNumber, 0)).pack(side="bottom", fill='both')

        def on_closing(orderNumber):  # x 표시를 누르면 창 닫힘
            if messagebox.askokcancel("Quit", "종료하시겠습니까?"):
                orderNumber.clear()
                orderNumber.append(-1)
                menuWindow.destroy()

        menuWindow.protocol("WM_DELETE_WINDOW", lambda: on_closing(orderNumber))
        menuWindow.mainloop()
        return orderNumber

    def printPayConfirm(self, totalPrice, chargedMoney):
        result = []
        global confirmWindow
        confirmWindow = Tk()
        confirmWindow.title("확인 창")
        confirmWindow.geometry("480x200+300+300")
        confirmWindow.resizable(False, False)
        moneyText = "총 결제금액: %d 회원님의 잔액 : %d" % (totalPrice, chargedMoney)
        confirmText = "결제하시겠습니까?"
        Label(confirmWindow, text=moneyText).pack(side="top", fill="both")
        Label(confirmWindow, text=confirmText).pack(side="top", fill="both")
        buttonFrame = Frame(confirmWindow)
        Button(buttonFrame, width=2, height=2, text="Y", command=lambda: self.interface.confirmCheck('Y', result)).pack(
            side="left")
        Button(buttonFrame, width=2, height=2, text="N", command=lambda: self.interface.confirmCheck('N', result)).pack(
            side="right")
        buttonFrame.pack(side="bottom")
        menuWindow.mainloop()

        return result.pop()

    def printFinish(self):
        noticeWindow = Tk()
        noticeWindow.title("결제 완료 창")
        noticeWindow.geometry("480x200+300+300")
        noticeWindow.resizable(False, False)
        noticeText = "결제가 완료되었습니다."
        Label(noticeWindow, text=noticeText).pack(side="top", fill="both")
        Button(noticeWindow, width=2, height=2, text="확인", command=lambda: noticeWindow.destroy()).pack(side="bottom",
                                                                                                        fill="both")
        menuWindow.mainloop()

    def printLack(self):
        noticeWindow = Tk()
        noticeWindow.title("잔액 부족 창")
        noticeWindow.geometry("480x200+300+300")
        noticeWindow.resizable(False, False)
        noticeText = "잔액이 부족합니다."
        Label(noticeWindow, text=noticeText).pack(side="top", fill="both")
        Button(noticeWindow, width=2, height=2, text="확인", command=lambda: noticeWindow.destroy()).pack(side="bottom",
                                                                                                        fill="both")
        menuWindow.mainloop()

    def printFailed(self):
        noticeWindow = Tk()
        noticeWindow.title("결제 취소 창")
        noticeWindow.geometry("480x200+300+300")
        noticeWindow.resizable(False, False)
        noticeText = "결제가 취소되었습니다."
        Label(noticeWindow, text=noticeText).pack(side="top", fill="both")
        Button(noticeWindow, width=2, height=2, text="확인", command=lambda: noticeWindow.destroy()).pack(side="bottom",
                                                                                                        fill="both")
        menuWindow.mainloop()

    def printRecharge(self):
        result = []
        global rechargeAskWindow
        rechargeAskWindow = Tk()
        rechargeAskWindow.title("잔액 충전 확인 창")
        rechargeAskWindow.geometry("480x200+300+300")
        rechargeAskWindow.resizable(False, False)
        questionText = "충전하시겠습니까?"
        Label(rechargeAskWindow, text=questionText).pack(side="top", fill="both")
        buttonFrame = Frame(rechargeAskWindow)
        Button(buttonFrame, width=2, height=2, text="Y",
               command=lambda: self.interface.rechargeConfirmCheck('Y', result)).pack(side="left")
        Button(buttonFrame, width=2, height=2, text="N",
               command=lambda: self.interface.rechargeConfirmCheck('N', result)).pack(side="right")
        buttonFrame.pack(side="bottom")
        menuWindow.mainloop()

        if result.pop():
            noticeWindow = Tk()
            noticeWindow.title("잔액 충전 창")
            noticeWindow.geometry("480x200+300+300")
            noticeWindow.resizable(False, False)
            noticeText = "잔액을 충전합니다."
            Label(noticeWindow, text=noticeText).pack(side="top", fill="both")
            Button(noticeWindow, width=2, height=2, text="확인", command=lambda: noticeWindow.destroy()).pack(
                side="bottom", fill="both")
            menuWindow.mainloop()

        else:
            noticeWindow = Tk()
            noticeWindow.title("결제 취소 창")
            noticeWindow.geometry("480x200+300+300")
            noticeWindow.resizable(False, False)
            noticeText = "결제가 취소되었습니다."
            Label(noticeWindow, text=noticeText).pack(side="top", fill="both")
            Button(noticeWindow, width=2, height=2, text="확인", command=lambda: noticeWindow.destroy()).pack(
                side="bottom", fill="both")
            menuWindow.mainloop()

    def makeError(self):
        noticeWindow = Tk()
        noticeWindow.title("에러")
        noticeWindow.geometry("480x200+300+300")
        noticeWindow.resizable(False, False)
        noticeText = "데이터베이스에 메뉴가 존재하지 않습니다."
        Label(noticeWindow, text=noticeText).pack(side="top", fill="both")
        Button(noticeWindow, width=2, height=2, text="확인", command=lambda: noticeWindow.destroy()).pack(side="bottom",
                                                                                                        fill="both")
        menuWindow.mainloop()

    def printEnterId(self):
        output = []
        global noticeWindow
        noticeWindow = Tk()
        noticeWindow.title("ID 입력")
        noticeWindow.geometry("250x160+300+300")
        noticeWindow.resizable(False, False)

        def on_closing(output):  # x 버튼 누르면 ID 입력 창 닫힘. 담은 메뉴들 초기화됨.
            if messagebox.askokcancel("Quit", "ID 입력을 종료하시겠습니까? \n 장바구니가 초기화됩니다."):
                output.clear()
                output.append(-1)
                noticeWindow.destroy()

        noticeWindow.protocol("WM_DELETE_WINDOW", lambda: on_closing(output))

        label = Label(noticeWindow, text='   ID를 입력하세요.')
        label.grid(row=0, column=3)

        id = StringVar()
        inputID = Entry(noticeWindow, width=15, textvariable=id)
        inputID.grid(row=1, column=3)

        def click(output):
            output.append(id.get())
            noticeWindow.destroy()

        button = Button(noticeWindow, text='입력', command=lambda: click(output))
        button.grid(row=1, column=4)
        noticeWindow.mainloop()
        # print("output type:", type(output))
        # print("output: ", output)
        return output[0]


class OrderStorage:
    def saveCustomerOrder(self, pnoList, menuList):
        self.pnoList = pnoList  # order storage에 주문서 저장
        sum = 0

        for menu in pnoList:
            for item in menuList:
                if menu == item.pno:  # 사용자가 선택한 메뉴가 메뉴 리스트에 있다면
                    sum += item.price  # 총 계산금액 계산
                    break

        self.totalPrice = sum

    def loadCustomerOrder(self):  # order storage에 저장된 주문서를 반환
        return self.pnoList


class Pay:
    def doCheckPayment(self, totalPrice, chargedMoney):
        if totalPrice <= chargedMoney:  # 유저 머니가 총 계산금액보다 크다면 user.money-> chargedMoney
            return True
        else:  # 잔액이 부족
            return False

    def payment(self, totalPrice, chargedMoney):
        if self.doCheckPayment(totalPrice, chargedMoney) == True:  # 유저머니가 충분하다면 user.money-> chargedMoney
            chargedMoney -= totalPrice  # 결제(유저머니  차감) user.money-> chargedMoney
            return chargedMoney  # return값 수정


class InterfacePage:
    def __init__(self):
        self.DB = DBConnection()

    def makeOrder(self, orderNumber, pno):
        if pno != 0:
            orderNumber.append(pno)
            # print(pno)

        else:
            menu = self.DB.getMenuList()
            print('장바구니')
            for order in orderNumber:
                for m in menu:
                    if order == m.pno:
                        print(m.name, m.price)
                        break
            menuWindow.destroy()

    def confirmCheck(self, answer, result):
        if answer == 'Y':
            result.append(True)
            confirmWindow.destroy()
        elif answer == 'N':
            result.append(False)
            confirmWindow.destroy()

    def rechargeConfirmCheck(self, answer, result):
        if answer == 'Y':
            result.append(True)
            rechargeAskWindow.destroy()
        elif answer == 'N':
            result.append(False)
            rechargeAskWindow.destroy()


class Controller:
    def __init__(self):
        self.DB = DBConnection()
        self.UIM = UIMaker()
        self.OS = OrderStorage()
        self.pay = Pay()

    def getMenuList(self):  # DB에서 메뉴 리스트 불러오기
        menuList = self.DB.getMenuList()
        return menuList

    def getUserChargedMoney(self, userId):
        userChargedMoney = self.DB.getUserChargedMoney(userId)
        return userChargedMoney

    def run(self):
        while (True):
            menuList = self.getMenuList()
            orderNumber = self.UIM.printMenu(menuList)  # UI로 메뉴 출력
            if orderNumber[0] == -1:
                break
            self.OS.saveCustomerOrder(orderNumber,
                                      menuList)  # order storage에 사용자가 주문한 메뉴의 번호 리스트(number)와 메뉴정보(가격 계산용) 저장

            next = True
            while (True):
                print()
                id = int(self.UIM.printEnterId())
                if id == -1:
                    next = False
                    break
                # id = int(input("id를 입력하세요. ")) # UIMaker (이 부분은 별도의 usecase가 있으므로 임의로)
                userChargedMoney = self.getUserChargedMoney(id)
                if userChargedMoney >= 0:
                    break

            #  *. 결제하기
            if next == False:
                continue  # 메뉴창으로 다시 이동
            totalPrice = self.OS.totalPrice
            if self.pay.doCheckPayment(totalPrice, userChargedMoney) == True:  # 잔액이 존재
                if self.UIM.printPayConfirm(totalPrice, userChargedMoney) == True:  # 결제진행을 원한다면
                    updatedMoney = self.pay.payment(totalPrice, userChargedMoney)
                    if updatedMoney >= 0:
                        self.DB.updateUserMoney(id, updatedMoney)
                        self.UIM.printFinish()

                    else:  # 결제실패(잔액부족)
                        self.UIM.printLack()

                else:  # 잔액이 존재하지만 결제는 원하지 않는 경우.
                    # (ex. 갑자기 결제하기 싫어졌을 때 or 메뉴를 변경하고 싶을 때 or
                    # continue  # 새 user?
                    self.UIM.printFailed()
                    # 이전 창으로 이동
            else:
                self.UIM.printLack()
                self.UIM.printRecharge()
                # continue # 잔액부족. 결제실패사유
                # 충전금액이 없을 때 창만 띄우면 되는 정도. 충전안내창. 충전: 임의적으로 user.money금액 더하고 pay함수 호출. NO: 종료


if __name__ == "__main__":
    controller = Controller()
    controller.run()