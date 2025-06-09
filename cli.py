from datetime import datetime
from models import Member, WorkoutSession
from database import get_session
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select

class MemberMenu:
    """Handles all CLI menu operations related to Members."""

    def __init__(self):
        pass

    def menu(self):
        while True:
            print("\n=== Member Management ===")
            print("1. Create Member")
            print("2. Delete Member")
            print("3. Display All Members")
            print("4. View Member's Workout Sessions")
            print("5. Find Member By Email")
            print("6. Back to Main Menu")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.create_member()
            elif choice == "2":
                self.delete_member()
            elif choice == "3":
                self.display_all_members()
            elif choice == "4":
                self.view_member_sessions()
            elif choice == "5":
                self.find_member_by_email()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please enter a number between 1-6.")

    def create_member(self):
        print("\n-- Create New Member --")
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        email = input("Email: ").strip()

        if not first_name or not last_name or not email:
            print("All fields are required.")
            return

        new_member = Member(first_name=first_name, last_name=last_name, email=email)

        with get_session() as session:
            session.add(new_member)
            try:
                session.commit()
                print(f"Member '{new_member.full_name}' created successfully with ID {new_member.member_id}.")
            except IntegrityError:
                session.rollback()
                print("Error: Email must be unique. That email is already registered.")
            except Exception as e:
                session.rollback()
                print(f"Failed to create member: {e}")

    def delete_member(self):
        print("\n-- Delete Member --")
        member_id = input("Enter member ID to delete: ").strip()
        if not member_id.isdigit():
            print("Invalid member ID. Must be a positive integer.")
            return

        member_id = int(member_id)
        with get_session() as session:
            member = session.get(Member, member_id)
            if member is None:
                print(f"No member found with ID {member_id}.")
                return

            confirm = input(f"Are you sure you want to delete member '{member.full_name}' and all their sessions? (y/n): ").strip().lower()
            if confirm == 'y':
                session.delete(member)
                session.commit()
                print(f"Member '{member.full_name}' deleted successfully.")
            else:
                print("Delete canceled.")

    def display_all_members(self):
        print("\n-- All Members --")
        with get_session() as session:
            members = session.execute(select(Member)).scalars().all()
            if not members:
                print("No members found.")
            else:
                for m in members:
                    print(f"ID: {m.member_id} | Name: {m.full_name} | Email: {m.email}")

    def view_member_sessions(self):
        print("\n-- View Member's Workout Sessions --")
        member_id = input("Enter member ID: ").strip()
        if not member_id.isdigit():
            print("Invalid member ID. Must be a positive integer.")
            return

        member_id = int(member_id)
        with get_session() as session:
            member = session.get(Member, member_id)
            if member is None:
                print(f"No member found with ID {member_id}.")
                return

            print(f"Workout sessions for {member.full_name}:")
            sessions = member.workout_sessions
            if not sessions:
                print("  No workout sessions recorded.")
                return

            for s in sessions:
                print(f"  Session ID: {s.session_id} | Date: {s.date} | Type: {s.workout_type} | Duration: {s.duration_minutes} min")

    def find_member_by_email(self):
        print("\n-- Find Member By Email --")
        email = input("Enter member email: ").strip()
        if not email:
            print("Email is required.")
            return

        with get_session() as session:
            try:
                stmt = select(Member).where(Member.email == email)
                member = session.execute(stmt).scalar_one()
                print(f"Found member: ID {member.member_id} | Name: {member.full_name} | Email: {member.email}")
            except NoResultFound:
                print("No member found with that email.")


class WorkoutSessionMenu:
    """Handles all CLI menu operations related to WorkoutSessions."""

    def __init__(self):
        pass

    def menu(self):
        while True:
            print("\n=== Workout Session Management ===")
            print("1. Add Workout Session")
            print("2. Delete Workout Session")
            print("3. Display All Workout Sessions")
            print("4. View Workout Session Detail")
            print("5. Find Workout Sessions By Date or Type")
            print("6. Update Workout Session Info")
            print("7. Back to Main Menu")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.add_workout_session()
            elif choice == "2":
                self.delete_workout_session()
            elif choice == "3":
                self.display_all_sessions()
            elif choice == "4":
                self.view_session_detail()
            elif choice == "5":
                self.find_sessions_by_date_or_type()
            elif choice == "6":
                self.update_session_info()
            elif choice == "7":
                break
            else:
                print("Invalid choice. Please enter a number between 1-7.")

    def add_workout_session(self):
        print("\n-- Add Workout Session --")
        member_id = input("Member ID: ").strip()
        date_str = input("Date (YYYY-MM-DD): ").strip()
        workout_type = input("Workout Type: ").strip()
        duration_str = input("Duration (minutes): ").strip()

        if not (member_id.isdigit() and date_str and workout_type and duration_str.isdigit()):
            print("Invalid input. Please provide valid member ID, date, workout type, and duration in minutes.")
            return

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

        member_id = int(member_id)
        duration = int(duration_str)

        with get_session() as session:
            member = session.get(Member, member_id)
            if member is None:
                print(f"No member found with ID {member_id}.")
                return

            new_session = WorkoutSession(
                member_id=member_id,
                date=date,
                workout_type=workout_type,
                duration_minutes=duration,
            )
            session.add(new_session)
            try:
                session.commit()
                print(f"Workout session added successfully with Session ID {new_session.session_id}.")
            except Exception as e:
                session.rollback()
                print(f"Failed to add workout session: {e}")

    def delete_workout_session(self):
        print("\n-- Delete Workout Session --")
        session_id = input("Enter session ID to delete: ").strip()
        if not session_id.isdigit():
            print("Invalid session ID. Must be a positive integer.")
            return

        session_id = int(session_id)
        with get_session() as session:
            workout_session = session.get(WorkoutSession, session_id)
            if workout_session is None:
                print(f"No workout session found with Session ID {session_id}.")
                return

            confirm = input(f"Are you sure you want to delete session {session_id}? (y/n): ").strip().lower()
            if confirm == 'y':
                session.delete(workout_session)
                session.commit()
                print(f"Workout session {session_id} deleted successfully.")
            else:
                print("Delete canceled.")

    def display_all_sessions(self):
        print("\n-- All Workout Sessions --")
        with get_session() as session:
            sessions = session.execute(select(WorkoutSession)).scalars().all()
            if not sessions:
                print("No workout sessions found.")
            else:
                for s in sessions:
                    print(f"Session ID: {s.session_id} | Member ID: {s.member_id} | Date: {s.date} | Type: {s.workout_type} | Duration: {s.duration_minutes} min")

    def view_session_detail(self):
        print("\n-- View Workout Session Detail --")
        session_id = input("Enter session ID: ").strip()
        if not session_id.isdigit():
            print("Invalid session ID. Must be a positive integer.")
            return

        session_id = int(session_id)
        with get_session() as session:
            workout_session = session.get(WorkoutSession, session_id)
            if workout_session is None:
                print(f"No workout session found with Session ID {session_id}.")
                return

            member = workout_session.member
            print(f"Session ID: {workout_session.session_id}")
            print(f"Member: {member.full_name} (ID {member.member_id})")
            print(f"Date: {workout_session.date}")
            print(f"Workout Type: {workout_session.workout_type}")
            print(f"Duration: {workout_session.duration_minutes} minutes")

    def find_sessions_by_date_or_type(self):
        print("\n-- Find Workout Sessions By Date or Type --")
        date_str = input("Enter date (YYYY-MM-DD) or leave blank to skip: ").strip()
        workout_type = input("Enter workout type or leave blank to skip: ").strip()

        filters = []
        with get_session() as session:
            stmt = select(WorkoutSession)
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    stmt = stmt.where(WorkoutSession.date == date)
                except ValueError:
                    print("Invalid date format. Use YYYY-MM-DD.")
                    return
            if workout_type:
                stmt = stmt.where(WorkoutSession.workout_type.ilike(f"%{workout_type}%"))

            results = session.execute(stmt).scalars().all()
            if not results:
                print("No workout sessions found matching criteria.")
            else:
                for s in results:
                    print(f"Session ID: {s.session_id} | Member ID: {s.member_id} | Date: {s.date} | Type: {s.workout_type} | Duration: {s.duration_minutes} min")

    def update_session_info(self):
        print("\n-- Update Workout Session Info --")
        session_id = input("Enter session ID to update: ").strip()
        if not session_id.isdigit():
            print("Invalid session ID. Must be a positive integer.")
            return

        session_id = int(session_id)
        with get_session() as session_db:
            workout_session = session_db.get(WorkoutSession, session_id)
            if workout_session is None:
                print(f"No workout session found with Session ID {session_id}.")
                return

            print(f"Current values (press Enter to keep current):")
            new_date = input(f"Date ({workout_session.date}): ").strip()
            new_type = input(f"Workout Type ({workout_session.workout_type}): ").strip()
            new_duration = input(f"Duration in minutes ({workout_session.duration_minutes}): ").strip()

            if new_date:
                try:
                    workout_session.date = datetime.strptime(new_date, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date format. Use YYYY-MM-DD.")
                    return
            if new_type:
                workout_session.workout_type = new_type
            if new_duration:
                if new_duration.isdigit() and int(new_duration) > 0:
                    workout_session.duration_minutes = int(new_duration)
                else:
                    print("Duration must be a positive integer.")
                    return

            try:
                session_db.commit()
                print("Workout session updated successfully.")
            except Exception as e:
                session_db.rollback()
                print(f"Failed to update session: {e}")


class GymCLIApp:
    """Main CLI app coordinating member and workout session menus."""

    def __init__(self):
        self.member_menu = MemberMenu()
        self.session_menu = WorkoutSessionMenu()

    def run(self):
        print("="*50)
        print("Welcome to the Gym Membership Tracker CLI App")
        print("="*50)

        while True:
            print("\nMain Menu:")
            print("1. Manage Members")
            print("2. Manage Workout Sessions")
            print("3. Exit")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.member_menu.menu()
            elif choice == "2":
                self.session_menu.menu()
            elif choice == "3":
                print("Goodbye! Thanks for using the Gym Membership Tracker.")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
