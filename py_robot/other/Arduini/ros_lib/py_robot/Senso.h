#ifndef _ROS_py_robot_Senso_h
#define _ROS_py_robot_Senso_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace py_robot
{

  class Senso : public ros::Msg
  {
    public:
      int64_t sensori[6];

    Senso():
      sensori()
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      for( uint32_t i = 0; i < 6; i++){
      union {
        int64_t real;
        uint64_t base;
      } u_sensorii;
      u_sensorii.real = this->sensori[i];
      *(outbuffer + offset + 0) = (u_sensorii.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_sensorii.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_sensorii.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_sensorii.base >> (8 * 3)) & 0xFF;
      *(outbuffer + offset + 4) = (u_sensorii.base >> (8 * 4)) & 0xFF;
      *(outbuffer + offset + 5) = (u_sensorii.base >> (8 * 5)) & 0xFF;
      *(outbuffer + offset + 6) = (u_sensorii.base >> (8 * 6)) & 0xFF;
      *(outbuffer + offset + 7) = (u_sensorii.base >> (8 * 7)) & 0xFF;
      offset += sizeof(this->sensori[i]);
      }
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      for( uint32_t i = 0; i < 6; i++){
      union {
        int64_t real;
        uint64_t base;
      } u_sensorii;
      u_sensorii.base = 0;
      u_sensorii.base |= ((uint64_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_sensorii.base |= ((uint64_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_sensorii.base |= ((uint64_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_sensorii.base |= ((uint64_t) (*(inbuffer + offset + 3))) << (8 * 3);
      u_sensorii.base |= ((uint64_t) (*(inbuffer + offset + 4))) << (8 * 4);
      u_sensorii.base |= ((uint64_t) (*(inbuffer + offset + 5))) << (8 * 5);
      u_sensorii.base |= ((uint64_t) (*(inbuffer + offset + 6))) << (8 * 6);
      u_sensorii.base |= ((uint64_t) (*(inbuffer + offset + 7))) << (8 * 7);
      this->sensori[i] = u_sensorii.real;
      offset += sizeof(this->sensori[i]);
      }
     return offset;
    }

    const char * getType(){ return "py_robot/Senso"; };
    const char * getMD5(){ return "2eacc918e609770d0b593ba5abcce269"; };

  };

}
#endif