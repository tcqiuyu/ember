package edu.colostate.ember.util;

public class LogUtil {

    public static void printErr(String msg) {
        System.out.println(StaticFields.ANSI_RED + msg + StaticFields.ANSI_RESET);
    }

    public static void printInfo(String msg) {
        System.out.println(StaticFields.ANSI_BLUE + msg + StaticFields.ANSI_RESET);
    }
    public static void printErr(int msg) {
        printErr(String.valueOf(msg));
    }
}
