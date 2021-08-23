using System;
using Xam_SmartHouse.Services;
using Xam_SmartHouse.Views;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace Xam_SmartHouse
{
    public partial class App : Application
    {
        public static string DatabaseMongo = string.Empty;
        public App()
        {
            InitializeComponent();

            DependencyService.Register<MockDataStore>();
            MainPage = new AppShell();
        }
        public App(string database)
        {
            InitializeComponent();
            DatabaseMongo = database;
            //MainPage = new NavigationPage(new ItemsPage());
            MainPage = new AppShell();
          
        }

        protected override void OnStart()
        {
        }

        protected override void OnSleep()
        {
        }

        protected override void OnResume()
        {
        }
    }
}
