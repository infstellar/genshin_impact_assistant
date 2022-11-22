using System.Runtime.InteropServices;

namespace cvAutoTrackCSharp
{
    internal class cvAutoTrack
    {
        [DllImport("cvAutoTrack.dll", EntryPoint = "verison")]
        public static extern bool verison(byte[] versionBuff);

        [DllImport("cvAutoTrack.dll", EntryPoint = "init")]
        public static extern bool init();

        [DllImport("cvAutoTrack.dll", EntryPoint = "uninit")]
        public static extern bool uninit();

        [DllImport("cvAutoTrack.dll", EntryPoint = "SetUseBitbltCaptureMode")]
        public static extern bool SetUseBitbltCaptureMode();

        [DllImport("cvAutoTrack.dll", EntryPoint = "SetUseDx11CaptureMode")]
        public static extern bool SetUseDx11CaptureMode();

        [DllImport("cvAutoTrack.dll", EntryPoint = "SetHandle")]
        public static extern bool SetHandle(long handle);

        [DllImport("cvAutoTrack.dll", EntryPoint = "SetWorldCenter")]
        public static extern bool SetWorldCenter(double x, double y);

        [DllImport("cvAutoTrack.dll", EntryPoint = "SetWorldScale")]
        public static extern bool SetWorldScale(double scale);

        [DllImport("cvAutoTrack.dll", EntryPoint = "GetTransformOfMap")]
        public static extern bool GetTransformOfMap(ref double x, ref double y, ref double a, ref int mapId);

        [DllImport("cvAutoTrack.dll", EntryPoint = "GetPositionOfMap")]
        public static extern bool GetPositionOfMap(ref double x, ref double y, ref int mapId);

        [DllImport("cvAutoTrack.dll", EntryPoint = "GetDirection")]
        public static extern bool GetDirection(ref double a);

        [DllImport("cvAutoTrack.dll", EntryPoint = "GetRotation")]
        public static extern bool GetRotation(ref double a);

        [DllImport("cvAutoTrack.dll", EntryPoint = "GetStar")]
        public static extern bool GetStar(ref double x, ref double y, ref bool isEnd);

        [DllImport("cvAutoTrack.dll", EntryPoint = "GetStarJson")]
        public static extern bool GetStarJson(byte[] jsonBuffer);

        [DllImport("cvAutoTrack.dll", EntryPoint = "GetUID")]
        public static extern bool GetUID(ref int uid);

        [DllImport("cvAutoTrack.dll", EntryPoint = "GetInfoLoadPicture")]
        public static extern bool GetInfoLoadPicture(byte[] path, ref int uid, ref double x, ref double y, ref double a);

        [DllImport("cvAutoTrack.dll", EntryPoint = "GetInfoLoadVideo")]
        public static extern bool GetInfoLoadVideo(byte[] path, byte[] pathOutFile);

        [DllImport("cvAutoTrack.dll", EntryPoint = "GetLastErr")]
        public static extern int GetLastErr();

        [DllImport("cvAutoTrack.dll", EntryPoint = "GetLastErrMsg")]
        public static extern int GetLastErrMsg(byte[] msg_buff, int buff_size); 
        
        [DllImport("cvAutoTrack.dll", EntryPoint = "GetLastErrJson")]
        public static extern int GetLastErrJson(byte[] json_buff, int buff_size);

        [DllImport("cvAutoTrack.dll", EntryPoint = "startServe")]
        public static extern bool startServe();

        [DllImport("cvAutoTrack.dll", EntryPoint = "stopServe")]
        public static extern bool stopServe();
        
        [DllImport("cvAutoTrack.dll", EntryPoint = "GetCompileVersion")]
        public static extern bool GetCompileVersion(byte[] version_buff, int buff_size);
        
        [DllImport("cvAutoTrack.dll", EntryPoint = "GetCompileTime")]
        public static extern bool GetCompileTime(byte[] time_buff, int buff_size);
        
    }
}
