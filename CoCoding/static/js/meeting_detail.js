// =====================================================================================================================
const C = 'c';
const JAVA = 'java';
const PYTHON = 'python';

const C_MODE = 'text/x-csrc';
const JAVA_MODE = 'text/x-java';
const PYTHON_MODE = 'python';

const C_TEMPLATE = `#include<stdio.h>

void main(){
    printf("hello C!");
}`;

const PYTHON_TEMPLATE = "print('hello python!')";

const JAVA_TEMPLATE = `public class Main {
    public static void main(String[] args) {
        System.out.println("Hello java!");
    }
}`;

const LANG_MAP = {
    [C]: {
        template: C_TEMPLATE,
        mode: C_MODE,
        name: 'C'
    },
    [JAVA]: {
        template: JAVA_TEMPLATE,
        mode: JAVA_MODE,
        name: 'Java'
    },
    [PYTHON]: {
        template: PYTHON_TEMPLATE,
        mode: PYTHON_MODE,
        name: 'Python'
    }
}
// =====================================================================================================================
const DISCARD_USER = 'discard_user';
const ADD_USER = 'add_user';
const MAKE_CALL = 'make_call';
const MAKE_ANSWER = 'make_answer';
const CHAT_MESSAGE = 'chat_message';
const CHANGE_CODE = 'edit_code';
const CHANGE_CANDIDATE = 'change_candidate'
const GET_CODE = 'get_code';

const configuration = {
    iceServers: [{'urls': 'stun:stun.l.google.com:19302'}]
}