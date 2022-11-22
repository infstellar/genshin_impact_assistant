#pragma once
#ifdef CVAUTOTRACK_EXPORTS
#define CVAUTOTRACK_PORT __declspec(dllexport)
#else
#define CVAUTOTRACK_PORT __declspec(dllimport)
#endif
#define CVAUTOTRACK_CALL __stdcall
#define CVAUTOTRACK_API CVAUTOTRACK_PORT CVAUTOTRACK_CALL


extern "C" bool CVAUTOTRACK_API verison(char* versionBuff);

extern "C" bool CVAUTOTRACK_API init();
extern "C" bool CVAUTOTRACK_API uninit();

extern "C" bool CVAUTOTRACK_API startServe();
extern "C" bool CVAUTOTRACK_API stopServe();

extern "C" bool CVAUTOTRACK_API SetUseBitbltCaptureMode();
extern "C" bool CVAUTOTRACK_API SetUseDx11CaptureMode();
extern "C" bool CVAUTOTRACK_API SetHandle(long long int handle);
extern "C" bool CVAUTOTRACK_API SetWorldCenter(double x, double y);
extern "C" bool CVAUTOTRACK_API SetWorldScale(double scale);

extern "C" bool CVAUTOTRACK_API GetTransformOfMap(double& x, double& y, double& a, int& mapId);
extern "C" bool CVAUTOTRACK_API GetPositionOfMap(double& x,double& y,int& mapId);
extern "C" bool CVAUTOTRACK_API GetDirection(double& a);
extern "C" bool CVAUTOTRACK_API GetRotation(double& a);
extern "C" bool CVAUTOTRACK_API GetStar(double &x, double &y, bool &isEnd);
extern "C" bool CVAUTOTRACK_API GetStarJson(char *jsonBuff);
extern "C" bool CVAUTOTRACK_API GetUID(int &uid);

extern "C" bool CVAUTOTRACK_API GetInfoLoadPicture(char* path, int &uid, double &x, double &y, double &a);
extern "C" bool CVAUTOTRACK_API GetInfoLoadVideo(char* path, char* pathOutFile);

extern "C" bool CVAUTOTRACK_API DebugCapture();
extern "C" bool CVAUTOTRACK_API DebugCapturePath(const char*path_buff, int buff_size);

extern "C" int  CVAUTOTRACK_API GetLastErr();
extern "C" int  CVAUTOTRACK_API GetLastErrMsg(char* msg_buff, int buff_size);
extern "C" int  CVAUTOTRACK_API GetLastErrJson(char* json_buff, int buff_size);

extern "C" bool CVAUTOTRACK_API GetCompileVersion(char* version_buff, int buff_size);
extern "C" bool CVAUTOTRACK_API GetCompileTime(char* time_buff, int buff_size);
