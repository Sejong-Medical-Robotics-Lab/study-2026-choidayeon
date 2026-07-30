#!/usr/bin/env python3
"""미션 4 : 기립 -> 오른팔 인사 -> 양손 인사 -> 복귀 시퀀스"""

import argparse
import time
from g1edu import G1Sim, LocoClient

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-hanger", action="store_true", help="걸이(거치대) 없이 바닥 기립 자세로 시작")
    ap.add_argument("--no-viewer", action="store_true", help="시뮬레이터 뷰어 창 띄우지 않음")
    ap.add_argument("--fast", action="store_true", help="동작 속도 빠르게 실행")
    args = ap.parse_args()

    hanger = not args.no_hanger
    sim = G1Sim(hanger=hanger, start_standing=not hanger)
    sim.start(viewer=not args.no_viewer, realtime=not args.fast)
    client = LocoClient(sim)
    x = 0.06 if args.fast else 1.0  # 대기 배율

    try:
        print("모드:", client.GetMode())
        if hanger:
            client.Damp()
            time.sleep(1.0 * x)
            print("기립 시작...")
            client.StandUp()
            print("기립 완료 대기 중...")
            # 기립이 완료되어 모드가 'balance_stand'로 바뀔 때까지 확실히 대기합니다.
            while client.GetMode() != "balance_stand":
                time.sleep(0.1) # 0.1초씩 기다리며 상태 확인
            print("기립 완료! (balance_stand 진입 확정)")
            time.sleep(1.0) # 자세 안정화를 위한 추가 대기

        print("동작 재생: 오른팔 인사 (wave)")
        client.PlayAction("wave")
        while client.ActionActive():
            time.sleep(0.1 * x)
        time.sleep(1.0 * x)
   
        while client.GetMode() != "balance_stand":
                time.sleep(0.1)
        print("기립 완료! (balance_stand 진입)")
            
        time.sleep(1.0 * x)

        # 2. 왼팔 인사 (hands_up 모션 활용 또는 고유 액션 이름)
        print("동작 재생: 왼팔 인사 (hands_up)")
        client.PlayAction("hands_up")
        while client.ActionActive():
            time.sleep(0.1 * x)
        time.sleep(1.0 * x)

        # 3. 양손 인사 (bow 또는 추가 액션)
        print("동작 재생: 양손 인사 (bow)")
        client.PlayAction("bow")
        while client.ActionActive():
            time.sleep(0.1 * x)
        time.sleep(1.0 * x)

        print("정리(Damp)...")

    except Exception as e:
        print("예외 발생:", e)
    finally:
        client.Damp()  # 어떤 일이 있어도 안전 마무리
        time.sleep(1.0 * x)
        print("종료 모드:", client.GetMode(), "| 에러:", client.GetLastError() or "없음")
        sim.stop()

if __name__ == "__main__":
    main()
