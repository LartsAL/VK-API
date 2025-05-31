from vk_service import fetch_user_profile, fetch_friends, fetch_albums
from config import VK_ACCESS_TOKEN


def display_user_info(identifier: str):
    if not VK_ACCESS_TOKEN:
        print("ERROR: VK access token is not configured!")
        print("You must create a .env file with VK_ACCESS_TOKEN=token")
        return

    print("Fetching user data...")
    user = fetch_user_profile(identifier)

    if not user:
        print(f"ERROR: User '{identifier}' not found or inaccessible")
        return

    user_id = user.get('id')
    full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}"

    if user.get('deactivated'):
        print(f"ERROR: Account {full_name} is deactivated. Reason: {user['deactivated']}")
        return

    print(f"\nUser: {full_name} (ID: {user_id})")

    print("\nOptions:")
    print("1. View friends")
    print("2. View photo albums")
    print("3. Main menu")
    while True:
        choice = input("\nChoose an option: ").strip()
        if choice == '1':
            display_friends(user_id, full_name)
        elif choice == '2':
            display_albums(user_id, full_name)
        elif choice == '3':
            return
        else:
            print("Invalid option")


def display_friends(user_id: int, user_name: str):
    print(f"Getting friends for {user_name}...")
    friends_data = fetch_friends(user_id)

    if not friends_data.get('count'):
        print(f"{user_name} has no friends or the list is private")
        return

    max_friends = friends_data['count']

    while True:
        friends_to_display = int(input(f"Enter number of friends to display ({min(max_friends, 100)} max): "))
        if friends_to_display < 1 or friends_to_display > max_friends:
            print("Invalid number")
        else:
            break

    friends = friends_data['items']
    print(f"First {friends_to_display} friends of {user_name} ({max_friends} total):")

    for i, friend in enumerate(friends[:friends_to_display], 1):
        friend_name = f"{friend['first_name']} {friend['last_name']}"
        status = " (deactivated)" if friend.get('deactivated') else ""
        print(f"{i}. {friend_name}{status}")


def display_albums(user_id: int, user_name: str):
    print(f"Getting albums for {user_name}...")
    albums = fetch_albums(user_id)

    if not albums:
        print(f"{user_name} has no albums or the list is private")
        return

    print(f"Albums of {user_name}:")
    for i, album in enumerate(albums, 1):
        size = album.get('size', 0)
        print(f"{i}. {album['title']} - {size} photos")


def main():
    while True:
        identifier = input("Enter VK user ID or username (or q to quit): ").strip()
        if identifier.lower() == 'q':
            break
        if identifier:
            display_user_info(identifier)


if __name__ == "__main__":
    main()