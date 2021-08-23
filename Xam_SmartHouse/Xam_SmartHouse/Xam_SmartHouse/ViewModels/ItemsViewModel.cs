using MongoDB.Bson;
using MongoDB.Driver;
using Plugin.LocalNotification;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using Xam_SmartHouse.Models;
using Xam_SmartHouse.Views;
using Xamarin.Forms;

namespace Xam_SmartHouse.ViewModels
{
    public class ItemsViewModel : BaseViewModel
    {
        private People _selectedItem;

        public bool status;

        public Random random;
        public ObservableCollection<People> Items { get; }
        public ObservableCollection<People> ItemsReference { get; }
        public ObservableCollection<People> ItemsCheck { get; }
        public Xamarin.Forms.Command LoadItemsCommand { get; }
        public Xamarin.Forms.Command AddItemCommand { get; }
        public Xamarin.Forms.Command<People> ItemTapped { get; }
        public NotificationRequest nr;

        public ItemsViewModel()
        {
            

            status = false;
            Title = "Browse";
            Items = new ObservableCollection<People>();
            ItemsReference = new ObservableCollection<People>();
            ItemsCheck = new ObservableCollection<People>();

            LoadItemsCommand = new Command(async () => await ExecuteLoadItemsCommand());

            ItemTapped = new Xamarin.Forms.Command<People>(OnItemSelected);

            AddItemCommand = new Command(OnAddItem);



            nr = new NotificationRequest();
           


        }


        

        async Task ExecuteLoadItemsCommand()
        {
           
            IsBusy = true;

            while (true)
            {

                try
                {


                    if (status)
                    {
                        ItemsCheck.Clear();
                        MongoClient dbClient = new MongoClient(App.DatabaseMongo);
                        var database = dbClient.GetDatabase("FaceRecognition");
                        var collection = database.GetCollection<BsonDocument>("project");

                        using (IAsyncCursor<BsonDocument> cursor = await collection.FindAsync(new BsonDocument()))
                        {


                            while (await cursor.MoveNextAsync())
                            {
                                IEnumerable<BsonDocument> batch = cursor.Current;

                                foreach (BsonDocument document in batch)
                                {

                                    string[] imgs = document.GetElement("name").Value.ToString().Split(' ');
                                    string img = imgs[0];

                                    ItemsCheck.Add(new People() { name = document.GetElement("name").Value.ToString(), time = document.GetElement("time").Value.ToString(), count = document.GetElement("count").Value.ToString(), color = document.GetElement("color").Value.ToString(), image = img });

                                }


                            }
                        }


                        foreach(People p in ItemsCheck)
                        {
                            People p2 = ItemsReference[ItemsCheck.IndexOf(p)];
                            if(p.count != p2.count || p.time != p2.time)
                            {


                                int i = 0;
                                foreach (People p3 in ItemsCheck)
                                {
                                   
                                    if(i == 0)
                                    {
                                        Items.Clear();
                                        ItemsReference.Clear();
                                        nr.BadgeNumber = 1;
                                        nr.Description = p.name;
                                        nr.Title = "Activity Detected";
                                        nr.ReturningData = "Dummy Data";
                                        nr.NotificationId = random.Next();
                                        nr.Schedule.NotifyTime = DateTime.Now.AddSeconds(1);

                                        NotificationCenter.Current.Show(nr);
                                    }
                                    
                                    i = 1;
                                    Items.Add(p3);
                                    ItemsReference.Add(p3);


                                }
                          
                                

                            }
                        }

                    }
                    else
                    {

                        MongoClient dbClient = new MongoClient(App.DatabaseMongo);
                        var database = dbClient.GetDatabase("FaceRecognition");
                        var collection = database.GetCollection<BsonDocument>("project");

                        using (IAsyncCursor<BsonDocument> cursor = await collection.FindAsync(new BsonDocument()))
                        {


                            while (await cursor.MoveNextAsync())
                            {
                                IEnumerable<BsonDocument> batch = cursor.Current;

                                foreach (BsonDocument document in batch)
                                {
                                    string[] imgs = document.GetElement("name").Value.ToString().Split(' ');
                                    string img = imgs[0];

                                    Items.Add(new People() { name = document.GetElement("name").Value.ToString(), time = document.GetElement("time").Value.ToString(), count = document.GetElement("count").Value.ToString(), color = document.GetElement("color").Value.ToString(), image = img });
                                    ItemsReference.Add(new People() { name = document.GetElement("name").Value.ToString(), time = document.GetElement("time").Value.ToString(), count = document.GetElement("count").Value.ToString(), color = document.GetElement("color").Value.ToString(), image = img });
                                }


                            }
                        }


                        status = true;
                    }

         
                    
                }
                catch (Exception ex)
                {
                    Debug.WriteLine(ex);
                }
                finally
                {
                    IsBusy = false;
                }


                await Task.Delay(100);

            }

            
             
           
        }

        public void OnAppearing()
        {
            IsBusy = true;
            SelectedItem = null;
        }

        public People SelectedItem
        {
            get => _selectedItem;
            set
            {
                SetProperty(ref _selectedItem, value);
                OnItemSelected(value);
            }
        }

        private async void OnAddItem(object obj)
        {
        }

        async void OnItemSelected(People item)
        {
            if (item == null)
                return;

            
            await Shell.Current.GoToAsync($"");
        }
    }
}