export class Users{
  private _id: number;

  public set id(value: number) {
    this._id = value;
  }

  public get id(): number {
    return this._id;
  }

  private _username: string;

  public set username(value: string) {
    this._username = value;
  }

  public get username(): string {
    return this._username;
  }

  private _password: string;

  public set password(value: string) {
    this._password = value;
  }

  public get password(): string {
    return this._password;
  }

  private _role: string;

  public set role(value: string) {
    this._role = value;
  }

  public get role(): string {
    return this._role;
  }

  private _phone: string;

  public set phone(value: string) {
    this._phone = value;
  }

  public get phone(): string {
    return this._phone;
  }

  constructor(id: number, username: string, password: string, role: string, phone: string) {
    this._id = id;
    this._username = username;
    this._password = password;
    this._role = role;
    this._phone = phone;
  }

}