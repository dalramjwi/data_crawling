from search.logic.x_crawling import x_crawling
from search.logic.fm_crawling import fm_crawling
from search.logic.dc_crawling import dc_crawling
from search.logic.google_crawling import google_crawling

def main():
    while True:
        print("1. 데이터 크롤링")
        print("2. 블로깅")
        choice = input("실행할 작업을 선택하세요 (종료: q): ")

        if choice == "q":
            break

        if choice == "1":
            while True:
                print("1. X 크롤링")
                print("2. FM 크롤링")
                print("3. DC 크롤링")
                print("4. Google 크롤링")
                sub_choice = input("크롤링 작업을 선택하세요 (뒤로: n): ")

                if sub_choice == "n":
                    break

                if sub_choice == "1":
                    x_crawling()
                elif sub_choice == "2":
                    fm_crawling()
                elif sub_choice == "3":
                    dc_crawling()
                elif sub_choice == "4":
                    google_crawling()
                else:
                    print("잘못된 선택입니다.")

        elif choice == "2":
            print("현재 블로깅 되지 않은 데이터가 00개 존재합니다.")
            print("블로깅 기능은 아직 구현되지 않았습니다.")
        else:
            print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()
