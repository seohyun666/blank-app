# streamlit 라이브러리를 불러옵니다.
import streamlit as st

# --- 초기 설정 ---
# 페이지 제목과 아이콘을 설정합니다.
st.set_page_config(page_title="나의 To-do List", page_icon="✅")

# 페이지의 제목을 중앙에 큰 글씨로 표시합니다.
st.title("📝 나의 To-do List")
st.write("---") # 구분선

# --- 세션 상태 초기화 ---
# 앱이 재실행되어도 데이터를 유지하기 위해 세션 상태를 사용합니다.
# 'tasks' 라는 키가 세션 상태에 없으면, 빈 리스트로 초기화합니다.
# 각 task는 {'description': '할 일 내용', 'completed': False} 형태의 딕셔너리입니다.
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# --- 함수 정의 ---
# 새로운 할 일을 추가하는 함수
def add_task():
    # 사용자가 입력한 텍스트를 가져옵니다. (st.session_state.new_task_input)
    new_task_description = st.session_state.new_task_input
    # 입력된 내용이 있을 경우에만 작업을 수행합니다.
    if new_task_description:
        # st.session_state.tasks 리스트에 새로운 할 일(딕셔너리)을 추가합니다.
        st.session_state.tasks.append({"description": new_task_description, "completed": False})
        # 입력 필드를 비웁니다.
        st.session_state.new_task_input = ""

# 할 일을 삭제하는 함수
def delete_task(task_index):
    # 지정된 인덱스의 할 일을 리스트에서 제거합니다.
    st.session_state.tasks.pop(task_index)

# 할 일의 완료 상태를 변경하는 함수
def toggle_task_completion(task_index):
    # 지정된 인덱스의 할 일의 'completed' 값을 반전시킵니다 (True -> False, False -> True).
    st.session_state.tasks[task_index]["completed"] = not st.session_state.tasks[task_index]["completed"]


# --- UI 구성 ---
# 새로운 할 일을 입력받는 텍스트 입력 필드
# placeholder: 입력 필드에 기본으로 표시되는 안내 문구
# on_change: 입력 필드의 내용이 변경될 때마다 add_task 함수를 호출 (Enter 키를 눌렀을 때)
# key: 이 위젯의 고유한 이름. 세션 상태에서 이 이름으로 값을 관리합니다.
st.text_input(
    "새로운 할 일을 입력하세요:",
    placeholder="여기에 할 일을 적고 Enter를 누르세요.",
    on_change=add_task,
    key='new_task_input'
)

st.write("---") # 구분선

# --- 할 일 목록 표시 ---
st.subheader("📋 할 일 목록")

# 할 일 목록이 비어있지 않다면, 목록을 화면에 표시합니다.
if st.session_state.tasks:
    # tasks 리스트를 순회하며 각 할 일과 인덱스를 가져옵니다.
    for index, task in enumerate(st.session_state.tasks):
        # 3개의 컬럼을 생성하여 각 위젯을 가로로 정렬합니다.
        col1, col2 = st.columns([0.1, 0.9])

        with col1:
            # 완료 여부를 표시하는 체크박스
            st.checkbox(
                "", # 체크박스 옆 라벨은 비워둡니다.
                value=task["completed"], # 현재 완료 상태를 체크박스에 반영
                on_change=toggle_task_completion, # 체크박스 상태가 바뀌면 함수 호출
                args=(index,), # 함수에 전달할 인자 (할 일의 인덱스)
                key=f"complete_{index}" # 고유한 키
            )

        with col2:
            # 할 일 내용과 삭제 버튼을 나란히 표시하기 위해 또 컬럼을 나눕니다.
            sub_col1, sub_col2 = st.columns([0.8, 0.2])
            with sub_col1:
                # 할 일이 완료되었다면, 취소선을 그어 표시합니다.
                if task["completed"]:
                    st.markdown(f"<span style='text-decoration: line-through; color: grey;'>{task['description']}</span>", unsafe_allow_html=True)
                # 완료되지 않았다면, 그대로 표시합니다.
                else:
                    st.write(task["description"])

            with sub_col2:
                 # 삭제 버튼
                st.button(
                    "삭제",
                    on_click=delete_task, # 버튼이 클릭되면 함수 호출
                    args=(index,), # 함수에 전달할 인자 (할 일의 인덱스)
                    key=f"delete_{index}" # 고유한 키
                )
else:
    # 할 일이 하나도 없으면 안내 문구를 표시합니다.
    st.info("아직 추가된 할 일이 없습니다.")


# --- 완료 메시지 ---
# 할 일 목록이 비어있지 않고, 모든 할 일이 완료되었는지 확인합니다.
if st.session_state.tasks and all(task["completed"] for task in st.session_state.tasks):
    st.balloons() # 풍선 애니메이션 효과
    st.success("모든 할 일을 완료했습니다! 축하합니다! 🎉")
    