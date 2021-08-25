using System;

using Android.App;
using Android.Content.PM;
using Android.Runtime;
using Android.OS;
using Plugin.LocalNotification;

namespace Xam_SmartHouse.Droid
{
    [Activity(Label = "Smart House", Icon = "@mipmap/icon", Theme = "@style/MainTheme", MainLauncher = true, ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation | ConfigChanges.UiMode | ConfigChanges.ScreenLayout | ConfigChanges.SmallestScreenSize )]
    public class MainActivity : global::Xamarin.Forms.Platform.Android.FormsAppCompatActivity
    {
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);

            NotificationCenter.CreateNotificationChannel();

            Xamarin.Essentials.Platform.Init(this, savedInstanceState);
            global::Xamarin.Forms.Forms.Init(this, savedInstanceState);
            //string dbmongo = "mongodb+srv://zakariafaizi:projetpfc123@clusterpfc.efa6c.mongodb.net/FaceRecognition";
            string dbmongo = "mongodb://zakariafaizi:projetpfc123@clusterpfc-shard-00-00.efa6c.mongodb.net:27017,clusterpfc-shard-00-01.efa6c.mongodb.net:27017,clusterpfc-shard-00-02.efa6c.mongodb.net:27017/FaceRecognition?ssl=true&replicaSet=atlas-3ryp5k-shard-0&authSource=admin&retryWrites=true&w=majority";
            //string folderPath = System.Environment.GetFolderPath(System.Environment.SpecialFolder.Personal);
            LoadApplication(new App(dbmongo));
        }
        public override void OnRequestPermissionsResult(int requestCode, string[] permissions, [GeneratedEnum] Android.Content.PM.Permission[] grantResults)
        {
            Xamarin.Essentials.Platform.OnRequestPermissionsResult(requestCode, permissions, grantResults);

            base.OnRequestPermissionsResult(requestCode, permissions, grantResults);
        }
    }
}