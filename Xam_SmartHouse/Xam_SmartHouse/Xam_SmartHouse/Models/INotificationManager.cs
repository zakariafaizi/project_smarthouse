using System;
using System.Collections.Generic;
using System.Text;

namespace Xam_SmartHouse.Models
{
    interface INotificationManager
    {
        event EventHandler NotificationReceived;
        void Initialize();
        void SendNotification(string title, string message, DateTime? notifyTime = null);
        void ReceiveNotification(string title, string message);
    }
}
